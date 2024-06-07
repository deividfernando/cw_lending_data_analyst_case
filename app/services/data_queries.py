from app import *
from app.models import *


class DataQueries:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def get_combined_data(self):
            query = self.session.query(
                ClientModel.user_id,
                ClientModel.status.label('client_status'),
                ClientModel.batch,
                ClientModel.credit_limit,
                ClientModel.interest_rate.label('client_interest_rate'),
                LoanModel.loan_id,
                LoanModel.created_at.label('loan_created_at'),
                LoanModel.due_at,
                LoanModel.paid_at,
                LoanModel.status.label('loan_status'),
                LoanModel.loan_amount,
                LoanModel.due_amount,
                LoanModel.amount_paid,
                LoanModel.tax
            ).join(LoanModel, ClientModel.user_id == LoanModel.user_id).statement

            df = pd.read_sql(query, engine)
            return df


    def get_data_description(self):
        clients_count = self.session.query(func.count(ClientModel.user_id)).scalar()
        loans_count = self.session.query(func.count(LoanModel.loan_id)).scalar()
        return {
            "clients_count": clients_count,
            "loans_count": loans_count
        }


    def get_best_month_loan_issuance(self):
        results = self.session.query(
            func.date_trunc('month', LoanModel.created_at).label('month'),
            func.count(LoanModel.loan_id).label('loan_count'),
            func.sum(LoanModel.loan_amount).label('total_amount')
        ).group_by('month').order_by(func.sum(LoanModel.loan_amount).desc()).all()
        
        return results
    
    
    def get_average_loan_amount_by_month(self):
        results = self.session.query(
            func.date_trunc('month', LoanModel.created_at).label('month'),
            func.count(LoanModel.loan_id).label('loan_count'),
            func.sum(LoanModel.loan_amount).label('total_amount')
        ).group_by(
            func.date_trunc('month', LoanModel.created_at)
        ).order_by(
            func.date_trunc('month', LoanModel.created_at)
        ).all()

        return results


    def get_batch_metrics(self):
        ClientAlias = aliased(ClientModel)
        LoanAlias = aliased(LoanModel)
        
        total_clients_by_batch = self.session.query(
            ClientAlias.batch,
            func.count(ClientAlias.user_id).label('total_clients')
        ).group_by(ClientAlias.batch).subquery()
        
        clients_with_loans_by_batch = self.session.query(
            ClientAlias.batch,
            func.count(func.distinct(LoanAlias.user_id)).label('clients_with_loans')
        ).join(LoanAlias, ClientAlias.user_id == LoanAlias.user_id).group_by(ClientAlias.batch).subquery()
        
        clients_with_paid_loans_by_batch = self.session.query(
            ClientAlias.batch,
            func.count(func.distinct(LoanAlias.user_id)).label('clients_with_paid_loans')
        ).join(LoanAlias, ClientAlias.user_id == LoanAlias.user_id).filter(LoanAlias.status == 'paid').group_by(ClientAlias.batch).subquery()
        
        total_loans_by_batch = self.session.query(
            ClientAlias.batch,
            func.count(LoanAlias.loan_id).label('total_loans'),
            func.avg(LoanAlias.loan_amount).label('avg_loan_amount_per_client')
        ).join(LoanAlias, ClientAlias.user_id == LoanAlias.user_id).group_by(ClientAlias.batch).subquery()
        
        results = self.session.query(
            total_clients_by_batch.c.batch,
            total_clients_by_batch.c.total_clients,
            func.coalesce(total_loans_by_batch.c.total_loans, 0).label('total_loans'),
            func.coalesce(total_loans_by_batch.c.avg_loan_amount_per_client, 0).label('avg_loan_amount_per_client'),
            func.coalesce((clients_with_loans_by_batch.c.clients_with_loans / total_clients_by_batch.c.total_clients) * 100, 0).label('percentage_clients_with_loans'),
            func.coalesce((clients_with_paid_loans_by_batch.c.clients_with_paid_loans / clients_with_loans_by_batch.c.clients_with_loans) * 100, 0).label('percentage_clients_with_paid_loans')
        ).outerjoin(
            clients_with_loans_by_batch, total_clients_by_batch.c.batch == clients_with_loans_by_batch.c.batch
        ).outerjoin(
            clients_with_paid_loans_by_batch, total_clients_by_batch.c.batch == clients_with_paid_loans_by_batch.c.batch
        ).outerjoin(
            total_loans_by_batch, total_clients_by_batch.c.batch == total_loans_by_batch.c.batch
        ).order_by(total_clients_by_batch.c.batch).all()
        
        return results


    def get_interest_rate_outcomes(self):
        results = self.session.query(
            ClientModel.interest_rate,
            func.count(LoanModel.loan_id).label('total_loans'),
            func.sum(case((LoanModel.status == 'default', 1), else_=0)).label('default_loans')
        ).join(LoanModel, ClientModel.user_id == LoanModel.user_id).group_by(ClientModel.interest_rate).all()
        
        return results


    def get_client_ranking(self, top_n=10):
        # Best Clients
        best_clients_query = self.session.query(
            ClientModel.user_id,
            func.sum(LoanModel.due_amount - LoanModel.loan_amount).label('net_return')
        ).join(LoanModel, ClientModel.user_id == LoanModel.user_id).filter(
            ClientModel.status == 'approved',
            LoanModel.status.in_(['paid', 'ongoing'])
        ).group_by(ClientModel.user_id).having(
            func.sum(case((LoanModel.status == 'default', 1), else_=0)) == 0
        ).order_by(func.sum(LoanModel.due_amount - LoanModel.loan_amount).desc()).limit(top_n).all()
        
        best_clients = [
            {
                'user_id': client.user_id,
                'net_return': client.net_return
            }
            for client in best_clients_query
        ]
        
        # Worst Clients
        worst_clients_query = self.session.query(
            ClientModel.user_id,
            func.sum(LoanModel.loan_amount - LoanModel.amount_paid).label('loss')
        ).join(LoanModel, ClientModel.user_id == LoanModel.user_id).filter(
            LoanModel.status == 'default',
            LoanModel.amount_paid < LoanModel.loan_amount
        ).group_by(ClientModel.user_id).order_by(func.sum(LoanModel.loan_amount - LoanModel.amount_paid).desc()).limit(top_n).all()
        
        worst_clients = [
            {
                'user_id': client.user_id,
                'loss': client.loss
            }
            for client in worst_clients_query
        ]
        
        return best_clients, worst_clients


    def get_overall_default_rate(self):
        result = self.session.query(
            func.count(LoanModel.loan_id).label('total_loans'),
            func.sum(case((LoanModel.status == 'default', 1), else_=0)).label('default_loans')
        ).one()
        
        total_loans = result.total_loans
        default_loans = result.default_loans
        default_rate = (default_loans / total_loans) * 100 if total_loans else 0
        
        return total_loans, default_loans, default_rate


    def get_default_rate_by_month_and_batch(self):
        results = self.session.query(
            func.date_trunc('month', LoanModel.created_at).label('month'),
            ClientModel.batch,
            func.count(LoanModel.loan_id).label('total_loans'),
            func.sum(case((LoanModel.status == 'default', 1), else_=0)).label('default_loans')
        ).join(LoanModel, ClientModel.user_id == LoanModel.user_id).group_by(func.date_trunc('month', LoanModel.created_at), ClientModel.batch).all()
        
        return results


    def get_overall_profitability_data(self):
        overall_default_rate = self.session.query(
            func.avg(case((LoanModel.status == 'default', 1), else_=0))
        ).scalar()
        
        results = self.session.query(
            func.sum(case((LoanModel.status == 'paid', LoanModel.amount_paid - LoanModel.loan_amount), else_=0)).label('realized_profit_paid'),
            func.sum(case((and_(LoanModel.status == 'ongoing', LoanModel.amount_paid > LoanModel.loan_amount), LoanModel.amount_paid - LoanModel.loan_amount), else_=0)).label('realized_profit_ongoing'),
            func.sum(case((LoanModel.status == 'default', LoanModel.loan_amount - LoanModel.amount_paid), else_=0)).label('loss'),
            func.sum(case((LoanModel.status == 'ongoing', LoanModel.due_amount - LoanModel.loan_amount), else_=0)).label('expected_profit_ongoing'),
            func.sum(LoanModel.due_amount - LoanModel.loan_amount).label('total_potential_profit')
        ).first()
        
        return results, overall_default_rate


    def get_profitability_data(self):
        results = self.session.query(
            func.date_trunc('month', LoanModel.created_at).label('month'),
            func.sum(case((LoanModel.status == 'paid', LoanModel.amount_paid - LoanModel.loan_amount), else_=0)).label('realized_profit_paid'),
            func.sum(case((and_(LoanModel.status == 'ongoing', LoanModel.amount_paid > LoanModel.loan_amount), LoanModel.amount_paid - LoanModel.loan_amount), else_=0)).label('realized_profit_ongoing'),
            func.sum(case((LoanModel.status == 'default', LoanModel.loan_amount - LoanModel.amount_paid), else_=0)).label('loss')
        ).group_by(func.date_trunc('month', LoanModel.created_at)).all()
        
        return results
