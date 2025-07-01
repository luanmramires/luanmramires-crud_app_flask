import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com categorias padrão
"""

from app import create_app, db
from app.models import User, Category, Income, Expense
from datetime import datetime, timedelta
from decimal import Decimal

def init_database():
    app = create_app()
    
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Verificar se já existe um usuário admin
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Criar usuário admin
            admin_user = User(
                username='admin',
                email='admin@example.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe!")
        
        # Criar categorias se não existirem
        categories_data = [
            {'name': 'Salário', 'type': 'income', 'color': '#28a745'},
            {'name': 'Investimentos', 'type': 'income', 'color': '#17a2b8'},
            {'name': 'Freelance', 'type': 'income', 'color': '#20c997'},
            {'name': 'Alimentação', 'type': 'expense', 'color': '#dc3545'},
            {'name': 'Transporte', 'type': 'expense', 'color': '#fd7e14'},
            {'name': 'Moradia', 'type': 'expense', 'color': '#6f42c1'},
            {'name': 'Saúde', 'type': 'expense', 'color': '#e83e8c'},
            {'name': 'Educação', 'type': 'expense', 'color': '#6c757d'},
            {'name': 'Lazer', 'type': 'expense', 'color': '#ffc107'},
            {'name': 'Outros', 'type': 'expense', 'color': '#6c757d'}
        ]
        
        for cat_data in categories_data:
            existing_category = Category.query.filter_by(name=cat_data['name']).first()
            if not existing_category:
                category = Category(
                    name=cat_data['name'],
                    type=cat_data['type'],
                    color=cat_data['color'],
                    user_id=admin_user.id
                )
                db.session.add(category)
        
        db.session.commit()
        print("Categorias criadas/verificadas com sucesso!")
        
        # Buscar categorias para usar nas transações
        salary_category = Category.query.filter_by(name='Salário', user_id=admin_user.id).first()
        investment_category = Category.query.filter_by(name='Investimentos', user_id=admin_user.id).first()
        food_category = Category.query.filter_by(name='Alimentação', user_id=admin_user.id).first()
        transport_category = Category.query.filter_by(name='Transporte', user_id=admin_user.id).first()
        housing_category = Category.query.filter_by(name='Moradia', user_id=admin_user.id).first()
        
        # Adicionar transações de teste para diferentes meses
        test_transactions = [
            # Junho 2025 (mês atual)
            {'type': 'income', 'description': 'Salário', 'amount': 4500.40, 'date': datetime(2025, 6, 15), 'category': salary_category},
            {'type': 'income', 'description': 'Dividendos MXRF11', 'amount': 10000.00, 'date': datetime(2025, 6, 23), 'category': investment_category},
            {'type': 'expense', 'description': 'Gasolina', 'amount': 500.00, 'date': datetime(2025, 6, 30), 'category': transport_category},
            
            # Maio 2025
            {'type': 'income', 'description': 'Salário', 'amount': 4500.00, 'date': datetime(2025, 5, 15), 'category': salary_category},
            {'type': 'income', 'description': 'Freelance Projeto A', 'amount': 2000.00, 'date': datetime(2025, 5, 20), 'category': investment_category},
            {'type': 'expense', 'description': 'Aluguel', 'amount': 1200.00, 'date': datetime(2025, 5, 5), 'category': housing_category},
            {'type': 'expense', 'description': 'Supermercado', 'amount': 800.00, 'date': datetime(2025, 5, 10), 'category': food_category},
            {'type': 'expense', 'description': 'Uber', 'amount': 300.00, 'date': datetime(2025, 5, 25), 'category': transport_category},
            
            # Abril 2025
            {'type': 'income', 'description': 'Salário', 'amount': 4500.00, 'date': datetime(2025, 4, 15), 'category': salary_category},
            {'type': 'income', 'description': 'Dividendos PETR4', 'amount': 500.00, 'date': datetime(2025, 4, 10), 'category': investment_category},
            {'type': 'expense', 'description': 'Aluguel', 'amount': 1200.00, 'date': datetime(2025, 4, 5), 'category': housing_category},
            {'type': 'expense', 'description': 'Restaurante', 'amount': 400.00, 'date': datetime(2025, 4, 18), 'category': food_category},
            
            # Março 2025
            {'type': 'income', 'description': 'Salário', 'amount': 4500.00, 'date': datetime(2025, 3, 15), 'category': salary_category},
            {'type': 'expense', 'description': 'Aluguel', 'amount': 1200.00, 'date': datetime(2025, 3, 5), 'category': housing_category},
            {'type': 'expense', 'description': 'Academia', 'amount': 150.00, 'date': datetime(2025, 3, 1), 'category': food_category},
        ]
        
        # Verificar se já existem transações para evitar duplicatas
        existing_transactions = Income.query.filter_by(user_id=admin_user.id).count() + Expense.query.filter_by(user_id=admin_user.id).count()
        
        if existing_transactions == 0:
            for transaction in test_transactions:
                if transaction['type'] == 'income':
                    income = Income(
                        description=transaction['description'],
                        amount=Decimal(str(transaction['amount'])),
                        date=transaction['date'],
                        category_id=transaction['category'].id,
                        user_id=admin_user.id
                    )
                    db.session.add(income)
                else:
                    expense = Expense(
                        description=transaction['description'],
                        amount=Decimal(str(transaction['amount'])),
                        date=transaction['date'],
                        category_id=transaction['category'].id,
                        user_id=admin_user.id
                    )
                    db.session.add(expense)
            
            db.session.commit()
            print("Transações de teste criadas com sucesso!")
        else:
            print("Transações já existem, pulando criação de dados de teste.")
        
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    init_database() 