from flask import Flask, send_file
from flask_restful import Resource, Api
from syntax_tree import SyntaxTreeBuilder
app = Flask(__name__)
api = Api(app)

class Tree(Resource):
    def __init__(self):
        self.builder = SyntaxTreeBuilder()

    def get(self, sentence):
        filename = self.builder.build(sentence)
        #return filename
        return send_file(filename, 'image/png')

api.add_resource(Tree, '/tree/<string:sentence>')
#api.add_resource()

if __name__ == '__main__':
    app.run(debug=True)
