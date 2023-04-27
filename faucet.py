import subprocess
import os, re, pwd
from flask import Flask, request, jsonify, redirect
import unicodedata
from web3 import Web3
import random
from hexbytes import HexBytes

app = Flask(__name__)

# FROM
FROM = os.getenv('PUBLIC_KEY','0x2d558F4633FF8011C27401c0070Fd1E981770B94')
FROM_PRIVATEKEY = os.getenv('PRIVATE_KEY','0x6ec4b834db4a9d1d36e21b5cee822ea28d0666a34741ae222f946fc3517ef73b')
FAUCET_VALUE = os.getenv('FAUCET_VALUE','5') # ether
RPC_URI = os.getenv('RPC_URI', 'https://bc4p.nowum.fh-aachen.de/blockchain')
# For real ETH: https://mainnet.infura.io/v3/
TITLE = os.getenv('FAUCET_TITLE','BC4P Faucet')
CHAIN_ID = os.getenv('CHAIN_ID','123321')
@app.route("/", methods=["GET"])
def home():
    return redirect("/faucet")

@app.route("/faucet/api/add_key", methods=["POST"])
def add_key():
    try:
        data = request.get_json(force=True)
        public_key = data.get('public_key')
#        if not data.get('node_name'):
#            raise Exception('node_name missing')
        if not data.get('public_key'):
            raise Exception('public_key missing')
        print(f"from: {FROM},to: {public_key}, value: {FAUCET_VALUE} ether")

        web3 = Web3(Web3.HTTPProvider(RPC_URI))
        nonce = web3.eth.get_transaction_count(FROM)
        gasPrice = web3.to_wei('100', 'gwei')
        value = web3.to_wei(FAUCET_VALUE, 'ether')

        tx = {
            'chainId': int(CHAIN_ID),
            'nonce': nonce,
            'to': HexBytes(public_key),
            'value': value,
            'gas': 2000000,
            'gasPrice': gasPrice
        }
        signed_tx = web3.eth.account.sign_transaction(tx, FROM_PRIVATEKEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)


    except Exception as e:
        error_msg = f'Error adding key: {e}'
        print(error_msg)
        return error_msg, 400

    return jsonify({"Message": "OK"}), 200

@app.route("/faucet", methods=["GET"])
def faucet():
    html = f'''
<html>
   <body>
       <div center style="width: 60%; margin: auto; height: 80%" >
        <h1 style="text-align:center;">{TITLE}</h1>
        <form id="key_form" action = "/faucet/api/add_key" method="POST" style="display: flex;flex-direction: column;">
            <span style="margin-bottom: 20px;">
                <label for="public_key">Wallet address</label><br>
                <input type="string" style="width: 100%;" id="public_key" name="public_key" value="" />
            </span>
            <input type="submit" value="Get your Tokens!">
        </form>
        <div id="msg_box"></div>
        </div>


   </body>
</html>
'''

    script = '''
<script>
var form = document.getElementById('key_form');
form.onsubmit = function(event){
        var xhr = new XMLHttpRequest();
        var formData = new FormData(form);
        //open the request
        xhr.open('POST','/faucet/api/add_key')
        xhr.setRequestHeader("Content-Type", "application/json");

        //send the form data
        xhr.send(JSON.stringify(Object.fromEntries(formData)));

        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                form.reset(); //reset form after AJAX success or do something else
                console.log(xhr.response)
                document.getElementById("msg_box").innerHTML = xhr.response;
            }
        }
        //Fail the onsubmit to avoid page refresh.
        return false;
    }
</script>
'''
    return html+script
# https://stackoverflow.com/a/69374442

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# to test:
#requests.post('http://localhost:8080/faucet/api/add_key', data= {'public_key': 120304054})
