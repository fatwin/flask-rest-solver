from flask import Blueprint, jsonify
from bson import json_util, ObjectId
from bson.errors import InvalidId
import dal as DAL
import solver

api_bp = Blueprint('api', __name__)


@api_bp.route('/scenarios/<scenario_id>')
def scenario_endpoint(scenario_id):
    try:
        object_id = ObjectId(scenario_id)
    except (InvalidId, TypeError) as e:
        # app.logger.warning(e)
        return jsonify(error='scenario id not valid'), 200
    else:
        result = json_util.dumps(
            DAL.get_collection('scenario').find({'_id': object_id}))
        return jsonify(result), 200


@api_bp.route('/solver/<scenario_id>')
def solver_endpoint(scenario_id):
    status = solver.run(scenario_id)
    return jsonify(status=status), 200
