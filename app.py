from flask import Flask, request, jsonify
import boto3
import os
import hashlib

app = Flask(__name__)

# AWS config
aws_config = Config(
    max_pool_connections=100,
    retries={'max_attempts': 3}
)

# Config AWS (assumes IAM role or environment vars already set)
dynamodb = boto3.resource('dynamodb',  region_name="eu-north-1")
table = dynamodb.Table("ProductAMIMap")

DEFAULT_INSTANCE_TYPE = "t3.small"

def generate_username(email, ip):
    if email:
        return email.replace("@", "_").replace(".", "_")
    else:
        hashed_ip = hashlib.sha1(ip.encode()).hexdigest()[:8]
        return f"usercurious_{hashed_ip}"

@app.route("/resolve-user-vm", methods=["GET"])
def resolve_user_vm():
    product_id = request.args.get("product_id")
    email = request.args.get("email", "")
    ipaddress = request.args.get("ipaddress", "")

    if not product_id or not ipaddress:
        return jsonify({"error": "Missing product_id or ipaddress"}), 400

    try:
        response = table.get_item(Key={"product_id": int(product_id)})
        item = response.get("Item")

        if not item or "ami" not in item:
            return jsonify({"error": f"AMI not found for product_id {product_id}"}), 404

        ami = item["ami"]
        username = generate_username(email, ipaddress)

        return jsonify({
            "ami": ami,
            "instance_type": DEFAULT_INSTANCE_TYPE,
            "username": username
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
