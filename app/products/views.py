import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, current_app
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from . import products_bp
from .forms import ProductForm

db_path = os.path.join(os.getcwd(), 'data', 'products.json')
db = TinyDB(db_path, encoding='utf-8')
products_table = db.table('products')
Product = Query()


def get_next_id():
    """Генерація наступного унікального числового ID."""
    items = products_table.all()
    if not items:
        return 1
    return max(item['id'] for item in items) + 1


def save_image(file):
    """Безпечне збереження зображення з унікальним ім'ям UUID."""
    if not file or not file.filename:
        return None
    
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)

    return f"uploads/products/{unique_filename}"


@products_bp.route('/')
def product_list():
    items = products_table.all()
    return render_template('products/products.html', products=items)


@products_bp.route('/add', methods=['GET', 'POST'])
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = save_image(form.image.data)

        new_product = {
            'id': get_next_id(),
            'name': form.name.data.strip(),
            'content': form.content.data.strip(),
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': int(form.quantity.data),
            'image': image_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        products_table.insert(new_product)
        flash(f"Товар «{new_product['name']}» успішно додано!", 'success')
        return redirect(url_for('products.product_list'))

    elif request.method == 'POST':
        flash('Будь ласка, перевірте правильність заповнення форми.', 'danger')

    return render_template('products/product_form.html', form=form, title='Додати товар')


@products_bp.route('/<int:id>')
def product_detail(id):
    product = products_table.get(Product.id == id)
    if product is None:
        abort(404)
    return render_template('products/detail_product.html', product=product)


@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def product_edit(id):
    product = products_table.get(Product.id == id)
    if product is None:
        abort(404)

    form = ProductForm()

    if request.method == 'GET':
        form.name.data = product.get('name')
        form.content.data = product.get('content')
        form.price.data = product.get('price')
        form.category.data = product.get('category')
        form.quantity.data = product.get('quantity')

    if form.validate_on_submit():
        image_path = product.get('image')
        if form.image.data:
            new_image = save_image(form.image.data)
            if new_image:
                image_path = new_image

        updated_data = {
            'name': form.name.data.strip(),
            'content': form.content.data.strip(),
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': int(form.quantity.data),
            'image': image_path
        }

        products_table.update(updated_data, Product.id == id)
        flash(f"Товар «{updated_data['name']}» успішно оновлено!", 'success')
        return redirect(url_for('products.product_detail', id=id))

    elif request.method == 'POST':
        flash('Будь ласка, виправте помилки у формі.', 'danger')

    return render_template(
        'products/product_form.html',
        form=form,
        title=f"Редагувати: {product.get('name')}",
        product=product
    )


@products_bp.route('/<int:id>/delete', methods=['POST'])
def product_delete(id):
    product = products_table.get(Product.id == id)
    if product is None:
        abort(404)

    products_table.remove(Product.id == id)
    flash(f"Товар «{product.get('name')}» видалено.", 'info')
    return redirect(url_for('products.product_list'))