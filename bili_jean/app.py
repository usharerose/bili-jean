"""
Backend application
"""
from flask import Flask, jsonify, request, Response

from .work_service import WorkService


def create_app():
    _app = Flask(__name__)
    return _app


app = create_app()


@app.route('/get_video_info', methods=['POST'])
def get_video_info() -> Response:
    payload = request.json or {}
    url = payload.get('url', '')
    return_season = True if payload.get('return_season') is True else False
    result = WorkService.get_work_meta(url, return_season)
    if not result:
        result = []
    return jsonify({'data': [item.dict() for item in result]})


if __name__ == '__main__':
    app.run()
