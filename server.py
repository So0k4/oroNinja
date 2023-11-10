from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'caracolito'


@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
        session['activities'] = []
        session['moves'] = 0
        session['win'] = False  # Variable para el bono Sensei

    return render_template('index.html')

@app.route('/process_money', methods=['POST'])
def process_money():
    building = request.form['building']
    activities = session['activities']
    earnings = 0

    # Calcula las ganancias o pérdidas
    if building == 'farm':
        earnings = random.randint(10, 20)
    elif building == 'cave':
        earnings = random.randint(5, 10)
    elif building == 'house':
        earnings = random.randint(2, 5)
    elif building == 'casino':
        earnings = random.randint(-50, 50)

    session['gold'] += earnings

    # Registra la actividad en el registro con color
    if earnings > 0:
        activity = f'Earned {earnings} gold from the {building}!'
        color = 'green'
    else:
        activity = f'Entered a casino and {'lost' if earnings < 0 else 'earned'} {abs(earnings)} gold... Ouch.'
        color = 'red'

    activities.insert(0, (activity, color))

    # Bono Sensei: Verifica si se cumple la condición de victoria
    if session['gold'] >= 500 and session['moves'] <= 15:
        session['win'] = True
    return redirect('/')

@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
