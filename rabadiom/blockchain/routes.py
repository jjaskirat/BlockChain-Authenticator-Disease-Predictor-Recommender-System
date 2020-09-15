from flask import render_template, Blueprint, flash, request

from rabadiom.blockchain.utils import BlockChain, Patient, Doctor, Transaction, EHR, Block
from rabadiom.models import Blockchain, User, Keys, Ehr

from rabadiom.blockchain import blockchain
#blockchain = BlockChain()

bchain = Blueprint('bchain', __name__)


@bchain.route("/BlockChain", methods=['GET', 'POST'])
def show_chain():
#    with app.app_context():
        rows = Blockchain.query.all()
        chain = []
        if rows:
            #chain = []
            for row in rows:
                user = User.query.filter_by(id=row.user_id).first()
                doc = User.query.filter_by(id=row.doctor_id).first()
                    
                pat_keys = Keys.query.filter_by(user_id=user.id).first()
                pat_keys = pat_keys.private_key
                doc_keys = Keys.query.filter_by(user_id=doc.id).first()
                doc_keys = doc_keys.private_key
                patient = Patient(name=user.name, private_key=pat_keys)
                doctor = Doctor(name=doc.name, private_key=doc_keys)
                ehr = Ehr.query.filter_by(id=row.node).first()
                data = ""
                data += ehr.diseases1 + ehr.diseases2 + ehr.diseases3 + ehr.test_or_med1 + ehr.test_or_med2 + ehr.test_or_med3 + ehr.test_or_med4 + ehr.test_or_med5 + ehr.test_or_med6 + ehr.test_or_med7 + ehr.causes1 + ehr.causes2 + ehr.causes3 + ehr.causes4 + ehr.causes5 + ehr.causes6 + ehr.causes7
                ehr = EHR(patient=user, doctor=doc, data=data)
                transaction = Transaction(patient=user, doctor=doctor, ehr=ehr.ToHash())
                block = Block(transaction=transaction, hash=row.hash, prev_hash=row.prev_hash, nonce=row.nonce, tstamp=row.tstamp)
                #blockchain.newBlock(Block)
                #if blockchain.isChainValid(chain):
                chain.append(block)

        #if blockchain.isChainValid(chain):
        #	flash("Chain is Valid", "success")
        #	return render_template('show_chain.html', title='BlockChain', chain = chain)
        #else:
        #	flash("Chain is Invalid", "danger")
        #	return render_template('show_chain.html', title='BlockChain', chain = chain)

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            last_block_hash = last_block.hash
            if block.prev_hash != last_block_hash:
                flash("prev hash != last block hash" + str(current_index))
                flash("Chain is invalid","danger")
                return render_template('show_chain.html', title='BlockChain', chain = chain)
            last_block = block
            current_index += 1
        flash("Chain is valid", "success")
        return render_template('show_chain.html', title='BlockChain', chain = chain)
        