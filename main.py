from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from security import api_required
from scraper import leetcode, gfg, codechef, codeforces
from model import User, db
import threading
import queue

function_dict = {
    'leetcode':leetcode,
    'gfg':gfg,
    'codechef':codechef,
    'codeforces':codeforces
}

results_queue = queue.Queue()
def execute_function(function, args):
    result = function(*args)
    results_queue.put(result)

def run_threads(functions, usernames):
    threads = []
    for func, username in zip(functions, usernames):
        thread = threading.Thread(target=execute_function, args=(function_dict[func], (username,)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        
    results = []
    while not results_queue.empty():
        result = results_queue.get()
        results.append(result)
    return results

app = Flask(__name__)
api = Api(app)

class Data(Resource):
    @api_required
    def post(self):
        data = request.get_json()
        function_list = data.get('functions', [])
        username_list = data.get('usernames', [])
        result = run_threads(function_list, username_list)
        return jsonify(result=result)
        
        
        
api.add_resource(Data, '/data')

if __name__ == "__main__":
    app.run()
