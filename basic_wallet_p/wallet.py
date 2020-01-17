from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def hello(self):
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            self.name = request.form['name']
        print(self.name)

        if form.validate():
            # Save the comment here.
            flash('Hello ' + self.name)
        else:
            flash('Error: All the form fields are required. ')

        return render_template('hello.html', form=form)


if __name__ == "__main__":
    app.run()
