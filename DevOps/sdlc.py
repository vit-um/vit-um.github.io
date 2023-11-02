import base64

# Define an array of strings representing the steps in a software development lifecycle
steps = ["plan", "code", "test", "delivery", "deploy", "monitor"]

# Loop through each step in the array and perform an operation
for step in steps:
    encoded_text = base64.b64encode(step.encode('utf-8'))
    # Perform some operation related to the current step 
    # print("b'",encoded_text.decode('utf-8'),"'")
    print("b'{}'".format(encoded_text.decode('utf-8')))
