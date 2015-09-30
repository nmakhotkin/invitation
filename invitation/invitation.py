# coding=utf-8

import json
import os

import flask
from flask import render_template


base_path = os.getcwd()
app = flask.Flask(__name__)
host = "0.0.0.0"
port = 80
invitation_filename = "/invitation/acknowledgements.txt"

map_str = open("invitation/mapping.json").read()
mapping = json.loads(map_str, "cp1251")

# http://seto4ka.hopto.org/a5288434-3be5-49cc-97d2


@app.route('/', methods=["GET"])
def provide_id():
    return render_template('no_invite_id.html')


@app.route('/<invite_id>', methods=["GET"])
def get_request(invite_id):
    name, male = resolve_name(invite_id)

    if name:
        return render_template(
            'invite.html',
            name=name,
            male=male,
            invite_id=invite_id
        )
    else:
        return render_template('no_invite_id.html')


@app.route('/<invite_id>', methods=['POST'])
def ack_invite(invite_id):
    with open(base_path + invitation_filename, 'r') as f:
        acked = f.read().decode().split(',')

    with open(base_path + invitation_filename, 'a') as f:
        if resolve_name(invite_id)[0] not in acked:
            f.write("%s," % resolve_name(invite_id)[0].encode("utf8"))

    return render_template('thanks.html')


def resolve_name(invite_id):
    result = mapping.get(invite_id)

    if result:
        return result
    else:
        return None, None


if __name__ == "__main__":
    app.run(host=host, port=port)
