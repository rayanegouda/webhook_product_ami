# webhook_product_ami
 guacamole aws dynamodb create-table \
    --table-name ProductAMIMap \
    --attribute-definitions AttributeName=product_id,AttributeType=N \
    --key-schema AttributeName=product_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

➜  guacamole aws dynamodb put-item \
    --table-name ProductAMIMap \
    --item '{
        "product_id": {"N": "469"},
        "ami": {"S": "ami-0085b1c5854ce0b18"}
    }'

➜  guacamole aws dynamodb scan --table-name ProductAMIMap
