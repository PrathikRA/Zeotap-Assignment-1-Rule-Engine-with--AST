from flask import Flask, render_template, request
from rule_engine import init_db, save_rule, create_rule, combine_rules, evaluate_rule, save_evaluation_result

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    age = int(request.form['age'])
    department = request.form['department']
    salary = int(request.form['salary'])
    experience = int(request.form['experience'])
    data = {"age": age, "department": department, "salary": salary, "experience": experience}

    # rule1 = "((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing')) and (salary > 50000 or experience > 5)"
    rule1 = "((age > 30 and department == 'Marketing')) and (salary > 20000 or experience > 5)"
    rule2 = "((age > 30 and department == 'Marketing')) and (salary > 20000 or experience > 5)"
    save_rule(rule1)
    save_rule(rule2)
    node1 = create_rule(rule1)
    node2 = create_rule(rule2)
    combined_node = combine_rules([rule1, rule2])
    result = evaluate_rule(combined_node, data)
    save_evaluation_result(data, result)

    emoji_result = '✅' if result else '❌'
    return render_template('index.html', result=emoji_result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)