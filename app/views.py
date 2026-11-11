import logging
from flask import render_template, request, redirect, url_for, flash, Blueprint
from .forms import ContactForm

logging.basicConfig(
    filename='form_data.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@main.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)

@main.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        logging.info(
            f"Нове повідомлення: Name='{form.name.data}', "
            f"Email='{form.email.data}', Phone='{form.phone.data}', "
            f"Subject='{form.subject.data}', Message='{form.message.data}'"
        )
        flash('Повідомлення успішно надіслано!', 'success')
        return redirect(url_for('main.contacts'))
    elif request.method == 'POST':
        flash('Будь ласка, виправте помилки у формі.', 'danger')
        
    return render_template('contacts.html', title='Контакти', form=form)