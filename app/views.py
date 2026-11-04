import logging
from flask import render_template, request, redirect, url_for, flash
from . import app
from .forms import ContactForm

logging.basicConfig(
    filename='form_data.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        logging.info(
            f"Нове повідомлення: Name='{form.name.data}', "
            f"Email='{form.email.data}', Phone='{form.phone.data}', "
            f"Subject='{form.subject.data}', Message='{form.message.data}'"
        )
        flash('Повідомлення успішно надіслано!', 'success')
        return redirect(url_for('contacts'))
    elif request.method == 'POST':
        flash('Будь ласка, виправте помилки у формі.', 'danger')
        
    return render_template('contacts.html', title='Контакти', form=form)