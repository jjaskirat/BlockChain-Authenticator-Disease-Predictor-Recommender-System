from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from rabadiom import db, login_manager, bcrypt
from rabadiom.models import Post, User, Ehr, Keys, Blockchain, SignedEhr
from rabadiom.posts.forms import PostForm
from functools import wraps
from rabadiom.blockchain.utils import Patient, Doctor, Block, EHR, Transaction
from rabadiom.blockchain import blockchain


def login_is_required(role = "ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            if ( (current_user.role != role) and (role != "ANY")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_is_required("Doctor")
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if blockchain.isChainValid(blockchain.chain):
            user = User.query.filter_by(username=form.userid.data).first()
            post = Ehr(doctor_id=current_user.id, user_id=int(user.id), diseases1 = form.diseases[0].data, diseases2 = form.diseases[1].data, diseases3 = form.diseases[2].data,
                        test_or_med1 = form.test_or_med[0].data, test_or_med2 = form.test_or_med[1].data, test_or_med3 = form.test_or_med[2].data,
                        test_or_med4 = form.test_or_med[3].data, test_or_med5 = form.test_or_med[4].data, test_or_med6 = form.test_or_med[5].data,
                        test_or_med7 = form.test_or_med[6].data,
                        causes1 = form.causes[0].data, causes2 = form.causes[1].data, causes3 = form.causes[2].data,
                        causes4 = form.causes[3].data, causes5 = form.causes[4].data, causes6 = form.causes[5].data,
                        causes7 = form.causes[6].data)
            ehr = post
            doc_keys = Keys.query.filter_by(user_id=current_user.id).first()
            doc_keys = doc_keys.private_key
            pat_keys = Keys.query.filter_by(user_id=user.id).first()
            pat_keys = pat_keys.private_key
            patient = Patient(name=user.name, private_key=pat_keys)
            doctor = Doctor(name=current_user.name, private_key=doc_keys)
            data = ""
            data += ehr.diseases1 + ehr.diseases2 + ehr.diseases3 + ehr.test_or_med1 + ehr.test_or_med2 + ehr.test_or_med3 + ehr.test_or_med4 + ehr.test_or_med5 + ehr.test_or_med6 + ehr.test_or_med7 + ehr.causes1 + ehr.causes2 + ehr.causes3 + ehr.causes4 + ehr.causes5 + ehr.causes6 + ehr.causes7
            ehr = EHR(patient=patient, doctor=doctor, data=data)
            transaction = Transaction(patient=patient, doctor=doctor, ehr=ehr.ToHash())
            block = Block(transaction=transaction)
            block = blockchain.newBlock(block)
            try:
                chain_block = Blockchain.query.order_by(Blockchain.node.desc()).first()
                if len(blockchain.chain) == 2:
                    chain_user = User.query.filter_by(id=chain_user.user_id).first()
                    chain_doc = User.query.filter_by(id=chain_doc.user_id).first()
                    doc_keys = Keys.query.filter_by(user_id=chain_doc.id).first()
                    doc_keys = doc_keys.private_key
                    pat_keys = Keys.query.filter_by(user_id=chain_user.id).first()
                    pat_keys = pat_keys.private_key
                    patient = Patient(name=chain_user.name, private_key=pat_keys)
                    doctor = Doctor(name=chain_doc.name, private_key=doc_keys)
                    transaction = Transaction(patient=patient, doctor=doctor, ehr=chain_block.ehr)
                    block = Block(transaction=transaction)
                    blockchain.chain[0] = block
                block.prev_hash = chain_block.hash
            except:
                pass
            db_block = Blockchain(user_id=user.id, doctor_id=current_user.id, ehr=ehr.ToHash(), hash=block.hash,
                prev_hash=block.prev_hash, nonce=block.nonce, tstamp=block.tstamp)
            diseases1 = doctor.Sign(form.diseases[0].data)
            diseases2 = doctor.Sign(form.diseases[1].data)
            diseases3 = doctor.Sign(form.diseases[2].data)
            test_or_med1 = doctor.Sign(form.test_or_med[0].data)
            causes1 = doctor.Sign(form.causes[0].data)
            test_or_med2 = doctor.Sign(form.test_or_med[1].data)
            causes2 = doctor.Sign(form.causes[1].data)
            test_or_med3 = doctor.Sign(form.test_or_med[2].data)
            causes3 = doctor.Sign(form.causes[2].data)
            test_or_med4 = doctor.Sign(form.test_or_med[3].data)
            causes4 = doctor.Sign(form.causes[3].data)
            test_or_med5 = doctor.Sign(form.test_or_med[4].data)
            causes5 = doctor.Sign(form.causes[4].data)
            test_or_med6 = doctor.Sign(form.test_or_med[5].data)
            causes6 = doctor.Sign(form.causes[5].data)
            test_or_med7 = doctor.Sign(form.test_or_med[6].data)
            causes7 = doctor.Sign(form.causes[6].data)
            diseases1 = patient.Encrypt(diseases1)
            diseases2 = patient.Encrypt(diseases2)
            diseases3 = patient.Encrypt(diseases3)
            test_or_med1 = patient.Encrypt(test_or_med1)
            causes1 = patient.Encrypt(causes1)
            test_or_med2 = patient.Encrypt(test_or_med2)
            causes2 = patient.Encrypt(causes2)
            test_or_med3 = patient.Encrypt(test_or_med3)
            causes3 = patient.Encrypt(causes3)
            test_or_med4 = patient.Encrypt(test_or_med4)
            causes4 = patient.Encrypt(causes4)
            test_or_med5 = patient.Encrypt(test_or_med5)
            causes5 = patient.Encrypt(causes5)
            test_or_med6 = patient.Encrypt(test_or_med6)
            causes6 = patient.Encrypt(causes6)
            test_or_med7 = patient.Encrypt(test_or_med7)
            causes7 = patient.Encrypt(causes7)

            encrypted = SignedEhr(diseases1 = diseases1, diseases2 = diseases2, diseases3 = diseases3,
                    test_or_med1 = test_or_med1, test_or_med2 = test_or_med2, test_or_med3 = test_or_med3,
                    test_or_med4 = test_or_med4, test_or_med5 = test_or_med5, test_or_med6 = test_or_med6,
                    test_or_med7 = test_or_med7,
                    causes1 = causes1, causes2 = causes2, causes3 = causes3,
                    causes4 = causes4, causes5 = causes5, causes6 = causes6,
                    causes7 = causes7)

            db.session.add(db_block)
            db.session.add(post)
            db.session.add(encrypted)
            db.session.commit()

            flash('Your post has been created!', 'success')
            return redirect(url_for('doc_main.home'))
        else:
            flash(str(blockchain.chain[-1].ToDict()))
            flash("BlockChain is not Valid", "danger")
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@login_required
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Ehr.query.get_or_404(post_id)
    doctor = User.query.filter_by(id=post.doctor_id).first()
    encrypted = SignedEhr.query.filter_by(id=post.id).first()
    doc_keys = Keys.query.filter_by(user_id=doctor.id).first()
    doc_keys = doc_keys.private_key
    pat_keys = Keys.query.filter_by(user_id=current_user.id).first()
    pat_keys = pat_keys.private_key
    patient = Patient(name=current_user.name, private_key=pat_keys)
    doc = Doctor(name=doctor.name, private_key=doc_keys)
    diseases1 = patient.Decrypt(encrypted.diseases1)
    diseases2 = patient.Decrypt(encrypted.diseases2)
    diseases3 = patient.Decrypt(encrypted.diseases3)
    test_or_med1 = patient.Decrypt(encrypted.test_or_med1)
    causes1 = patient.Decrypt(encrypted.causes1)
    test_or_med2 = patient.Decrypt(encrypted.test_or_med2)
    causes2 = patient.Decrypt(encrypted.causes2)
    test_or_med3 = patient.Decrypt(encrypted.test_or_med3)
    causes3 = patient.Decrypt(encrypted.causes3)
    test_or_med4 = patient.Decrypt(encrypted.test_or_med4)
    causes4 = patient.Decrypt(encrypted.causes4)
    test_or_med5 = patient.Decrypt(encrypted.test_or_med5)
    causes5 = patient.Decrypt(encrypted.causes5)
    test_or_med6 = patient.Decrypt(encrypted.test_or_med6)
    causes6 = patient.Decrypt(encrypted.causes6)
    test_or_med7 = patient.Decrypt(encrypted.test_or_med7)
    causes7 = patient.Decrypt(encrypted.causes7)

    diseases1 = doc.Verify(post.diseases1, diseases1)
    diseases2 = doc.Verify(post.diseases2, diseases2)
    diseases3 = doc.Verify(post.diseases3, diseases3)
    test_or_med1 = doc.Verify(post.test_or_med1, test_or_med1)
    causes1 = doc.Verify(post.causes1, causes1)
    test_or_med2 = doc.Verify(post.test_or_med2, test_or_med2)
    causes2 = doc.Verify(post.causes2, causes2)
    test_or_med3 = doc.Verify(post.test_or_med3, test_or_med3)
    causes3 = doc.Verify(post.causes3, causes3)
    test_or_med4 = doc.Verify(post.test_or_med4, test_or_med4)
    causes4 = doc.Verify(post.causes4, causes4)
    test_or_med5 = doc.Verify(post.test_or_med5, test_or_med5)
    causes5 = doc.Verify(post.causes5, causes5)
    test_or_med6 = doc.Verify(post.test_or_med6, test_or_med6)
    causes6 = doc.Verify(post.causes6, causes6)
    test_or_med7 = doc.Verify(post.test_or_med7, test_or_med7)
    causes7 = doc.Verify(post.causes7, causes7)

    if diseases3 and diseases2 and diseases1 and test_or_med1 and test_or_med2 and test_or_med3 and test_or_med4 and test_or_med5 and test_or_med6 and test_or_med7 \
        and causes7 and causes6 and causes5 and causes4 and causes3 and causes2 and causes1:
        flash("OKAY ALL GOOD, DATA HAS NOT BEEN TAMPERED WITH", "success")
    else:
        flash("DANGER CONTENT IS INVALID")

    return render_template('post.html', title=post.id, post=post, doctor=doctor)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    flash("POST CAN NOT BE UPDATED ONCE ENTERED", "danger")
    return render_template('errors/403.html')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    flash("POST CAN NOT BE DELETED ONCE ENTERED", "danger")
    return render_template('errors/403.html')
