from app.services import *


class Visualization:
    def display_combined_data_sample(self, df):
        sample_df = df.sample(10)
        display(sample_df)
        
    
    def plot_loan_issuance_trend(self, data):
        df = pd.DataFrame(data, columns=['month', 'loan_count', 'total_amount'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        scale = 1000 if df['total_amount'].max() > 1e6 else 1
        scale_label = '($ thousands)' if scale == 1000 else ''

        df['total_amount_scaled'] = df['total_amount'] / scale

        _, ax1_line = plt.subplots(figsize=(16, 7))
        ax1_line.set_xlabel('Month')
        ax1_line.set_ylabel('Loan Count', color='tab:blue')
        ax1_line.plot(df.index, df['loan_count'], color='tab:blue', marker='o', label='Loan Count')
        ax1_line.tick_params(axis='y', labelcolor='tab:blue')
        ax1_line.set_xticks(df.index)
        ax1_line.set_xticklabels(df.index.strftime('%Y-%m'), rotation=90)

        ax2_line = ax1_line.twinx()
        ax2_line.set_ylabel(f'Total Amount {scale_label}', color='tab:orange')
        ax2_line.plot(df.index, df['total_amount_scaled'], color='tab:orange', marker='o', label='Total Amount')
        ax2_line.tick_params(axis='y', labelcolor='tab:orange')

        ax1_line.legend(loc='upper left')
        ax2_line.legend(loc='lower right')
        ax1_line.set_title('Best Month in Terms of Loan Issuance')

        plt.tight_layout()
        plt.show()
        
        
    def plot_average_loan_amount_by_month(self, data):
        df = pd.DataFrame(data, columns=['month', 'loan_count', 'total_amount'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        df['average_loan_amount'] = df['total_amount'] / df['loan_count']
        
        _, ax = plt.subplots(figsize=(16, 7))
        bars = ax.bar(df.index.strftime('%Y-%m'), df['average_loan_amount'], color='tab:blue')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f"${yval:,.2f}", ha='center', va='bottom', fontsize=8)

        ax.set_xlabel('Month')
        ax.set_ylabel('Average Loan Amount ($)')
        ax.set_title('Average Loan Amount by Month')
        ax.set_xticks(range(len(df.index)))
        ax.set_xticklabels(df.index.strftime('%Y-%m'), rotation=90)

        plt.tight_layout()
        plt.show()


    def plot_average_loan_amount_by_month(self, data):
        df = pd.DataFrame(data, columns=['month', 'loan_count', 'total_amount'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        df['average_loan_amount'] = df['total_amount'] / df['loan_count']

        _, ax = plt.subplots(figsize=(16, 7))
        _ = ax.bar(df.index.strftime('%Y-%m'), df['average_loan_amount'], color='tab:blue')

        ax.set_xlabel('Month')
        ax.set_ylabel('Average Loan Amount ($)')
        ax.set_title('Average Loan Amount by Month')
        ax.set_xticks(range(len(df.index)))
        ax.set_xticklabels(df.index.strftime('%Y-%m'), rotation=90)

        plt.tight_layout()
        plt.show()


    def plot_top_loan_months(self, data):
        df = pd.DataFrame(data, columns=['month', 'loan_count', 'total_amount'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        scale = 1000 if df['total_amount'].max() > 1e6 else 1
        scale_label = '($ thousands)' if scale == 1000 else ''

        df['total_amount_scaled'] = df['total_amount'] / scale

        top_loan_count = df.nlargest(5, 'loan_count').sort_values(by='loan_count')
        top_total_amount = df.nlargest(5, 'total_amount').sort_values(by='total_amount')

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

        ax1.barh(top_loan_count.index.strftime('%Y-%m'), top_loan_count['loan_count'], color='tab:blue', height=0.4, align='center', label='Loan Count')
        ax1.barh(top_loan_count.index.strftime('%Y-%m'), top_loan_count['total_amount_scaled'], color='tab:orange', height=0.4, align='edge', label='Total Amount')
        for i, (loan_count, total_amount) in enumerate(zip(top_loan_count['loan_count'], top_loan_count['total_amount_scaled'])):
            ax1.text(loan_count + 0.2, i - 0.1, f"{loan_count:,.0f}", color='blue', va='center')
            ax1.text(total_amount + 0.2, i + 0.1, f"${total_amount:,.2f}", color='black', va='center', ha='right')
        ax1.set_title('Top 5 Months with the Highest Number of Loans')
        ax1.set_xlabel('Amount')
        ax1.set_ylabel('Month')
        ax1.legend(loc='best')

        ax2.barh(top_total_amount.index.strftime('%Y-%m'), top_total_amount['loan_count'], color='tab:blue', height=0.4, align='center', label='Loan Count')
        ax2.barh(top_total_amount.index.strftime('%Y-%m'), top_total_amount['total_amount_scaled'], color='tab:orange', height=0.4, align='edge', label='Total Amount')
        for i, (loan_count, total_amount) in enumerate(zip(top_total_amount['loan_count'], top_total_amount['total_amount_scaled'])):
            ax2.text(loan_count + 0.2, i - 0.1, f"{loan_count:,.0f}", color='blue', va='center')
            ax2.text(total_amount + 0.2, i + 0.1, f"${total_amount:,.2f}", color='black', va='center', ha='right')
        ax2.set_title('Top 5 Months with the Highest Loan Amount')
        ax2.set_xlabel(f'Amount / Value {scale_label}')
        ax2.set_ylabel('Month')
        ax2.legend(loc='best')

        plt.tight_layout()
        plt.show()
    
    def plot_pie_charts(self, data):
        df = pd.DataFrame(data)

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        wedges1, _, _ = ax1.pie(df['total_clients'], autopct=lambda p: '{:.0f}'.format(p * sum(df['total_clients']) / 100), startangle=90)
        ax1.set_title('Number of Clients per Batch')
        ax1.legend(wedges1, df['batch'], title="Batch", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        wedges2, _, _ = ax2.pie(df['total_loans'], autopct=lambda p: '{:.0f}'.format(p * sum(df['total_loans']) / 100), startangle=90)
        ax2.set_title('Number of Loans per Batch')
        ax2.legend(wedges2, df['batch'], title="Batch", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        plt.show()


    def plot_batch_metrics(self, data):
        df = pd.DataFrame(data)

        df['avg_loan_amount_per_client'] = df['avg_loan_amount_per_client'].astype(float)
        df['percentage_clients_with_loans'] = df['percentage_clients_with_loans'].astype(float)
        df['percentage_clients_with_paid_loans'] = df['percentage_clients_with_paid_loans'].astype(float)

        _, ax = plt.subplots(figsize=(15, 6))

        width = 0.2
        x = range(len(df['batch']))

        avg_loan_per_client = df['total_loans'] / df['total_clients']

        ax.bar([p - width for p in x], avg_loan_per_client, width, label='Average Loan per Client')
        ax.bar(x, df['percentage_clients_with_loans'], width, label='Percentage of Clients with Loans')
        ax.bar([p + width for p in x], df['percentage_clients_with_paid_loans'], width, label='Percentage of Clients with Paid Loans')

        for i in x:
            ax.text(i - width, avg_loan_per_client[i] + 0.5, f"{avg_loan_per_client[i]:.2f}", ha='center', va='bottom')
            ax.text(i, df['percentage_clients_with_loans'][i] + 0.5, f"{df['percentage_clients_with_loans'][i]:.2f}%", ha='center', va='bottom')
            ax.text(i + width, df['percentage_clients_with_paid_loans'][i] + 0.5, f"{df['percentage_clients_with_paid_loans'][i]:.2f}%", ha='center', va='bottom')

        ax.set_xlabel('Batch')
        ax.set_ylabel('Values')
        ax.set_title('Metrics by Batch')
        ax.set_xticks(x)
        ax.set_xticklabels(df['batch'])
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

        plt.tight_layout()
        plt.show()


    def plot_best_batch_adherence(self, data):
        df = pd.DataFrame(data, columns=['batch', 'client_count', 'loan_count'])
        df['adherence_rate'] = df['loan_count'] / df['client_count']

        plt.figure(figsize=(10, 6))
        plt.bar(df['batch'], df['adherence_rate'], color='tab:blue')
        plt.xlabel('Batch')
        plt.ylabel('Adherence Rate')
        plt.title('Best Batch Adherence')
        plt.show()

    def plot_interest_rate_outcomes(self, data):
        df = pd.DataFrame(data, columns=['interest_rate', 'total_loans', 'default_loans'])
        df['default_rate'] = (df['default_loans'] / df['total_loans']) * 100

        df_with_default = df[df['default_loans'] > 0]

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        width = 0.4
        x = range(len(df['interest_rate']))

        total_loans_scaled = df['total_loans'] / df['total_loans'].max() * 100

        ax1.bar(x, total_loans_scaled, width, label='Total Loans', color='tab:blue')
        ax1.bar([p + width for p in x], df['default_rate'], width, label='Default Rate', color='tab:red')

        for i in range(len(df)):
            ax1.text(i, total_loans_scaled[i] + 1, f"{df['total_loans'][i]}", ha='center', va='bottom', color='black')
            ax1.text(i + width, df['default_rate'][i] + 1, f"{df['default_rate'][i]:.2f}%", ha='center', va='bottom', color='black')

        ax1.set_xlabel('Interest Rate (%)')
        ax1.set_ylabel('Amount / Default Rate (%)')
        ax1.set_title('Loans and Default Rate by Interest Rate')
        ax1.set_xticks([p + width / 2 for p in x])
        ax1.set_xticklabels(df['interest_rate'])
        ax1.legend()

        ax2.pie(df_with_default['default_loans'], labels=None, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Default Rate by Interest Rate')
        ax2.legend(df_with_default['interest_rate'], title="Interest Rate", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        plt.show()


    def display_client_tables(self, best_clients, worst_clients):
        best_df = pd.DataFrame(best_clients)
        worst_df = pd.DataFrame(worst_clients)

        best_df.columns = ['Client ID', 'Profit']
        worst_df.columns = ['Client ID', 'Loss']

        worst_df['Loss'] = worst_df['Loss'].fillna(0)
        
        best_df['Profit'] = best_df['Profit'].apply(lambda x: f"${x:,.2f}")
        worst_df['Loss'] = worst_df['Loss'].apply(lambda x: f"${x:,.2f}")

        best_html = best_df.style.set_caption('Best Clients').to_html()
        worst_html = worst_df.style.set_caption('Worst Clients').to_html()

        display_html(f'<div style="display: flex; justify-content: space-around;">{best_html}{worst_html}</div>', raw=True)

    def plot_client_ranking(self, best_clients, worst_clients):
        self.display_client_tables(best_clients, worst_clients)
        
        best_df = pd.DataFrame(best_clients)
        worst_df = pd.DataFrame(worst_clients)

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        best_df.plot(kind='bar', x='user_id', y='net_return', ax=ax1, color='tab:green', legend=False)
        ax1.set_title('Top 10 Best Clients')
        ax1.set_xlabel('Client ID')
        ax1.set_ylabel('Profit')

        worst_df.plot(kind='bar', x='user_id', y='loss', ax=ax2, color='tab:red', legend=False)
        ax2.set_title('Top 10 Worst Clients')
        ax2.set_xlabel('Client ID')
        ax2.set_ylabel('Loss')

        plt.tight_layout()
        plt.show()


    def plot_overall_default_rate(self, total_loans, default_loans, default_rate):
        _, ax = plt.subplots(figsize=(18, 5))

        data = {'Total Loans': total_loans, 'Default Loans': default_loans, 'Default Rate (%)': default_rate}
        bars = ax.bar(data.keys(), data.values(), color=['tab:blue', 'tab:red', 'tab:orange'])

        for bar in bars:
            yval = bar.get_height()
            if bar.get_label() == 'Default Rate (%)':
                ax.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.2f}%", ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, yval, f"{int(yval):,}", ha='center', va='bottom')

        ax.set_title('Overall Default Rate')
        plt.tight_layout()
        plt.show()

    def plot_default_rate_by_month_and_batch(self, data):
        df = pd.DataFrame(data, columns=['month', 'batch', 'total_loans', 'default_loans'])
        df['default_rate'] = (df['default_loans'] / df['total_loans']) * 100
        df['month'] = pd.to_datetime(df['month']).dt.strftime('%Y-%m')

        all_batches = df['batch'].unique()
        all_months = sorted(df['month'].unique())
        df_full = pd.DataFrame([(month, batch) for month in all_months for batch in all_batches], columns=['month', 'batch']).merge(df, on=['month', 'batch'], how='left').fillna(0)

        _, ax1 = plt.subplots(figsize=(18, 5))

        width = 0.2
        x = range(len(all_months))

        for i, batch in enumerate(all_batches):
            batch_data = df_full[df_full['batch'] == batch]
            ax1.bar([p + width*i for p in x], batch_data['default_rate'], width, label=f'Batch {batch}')

        ax1.set_xlabel('Month')
        ax1.set_ylabel('Default Rate (%)')
        ax1.set_title('Average Default Rate by Month and Batch')
        ax1.set_xticks([p + width*(len(all_batches)/2 - 0.5) for p in x])
        ax1.set_xticklabels(all_months, rotation=90)
        ax1.legend()

        _, ax2 = plt.subplots(figsize=(18, 5))

        for i, batch in enumerate(all_batches):
            batch_data = df_full[df_full['batch'] == batch]
            ax2.bar([p + width*i for p in x], batch_data['default_loans'], width, label=f'Batch {batch}')

        ax2.set_xlabel('Month')
        ax2.set_ylabel('Number of Defaulted Loans')
        ax2.set_title('Number of Defaulted Loans by Month and Batch')
        ax2.set_xticks([p + width*(len(all_batches)/2 - 0.5) for p in x])
        ax2.set_xticklabels(all_months, rotation=90)
        ax2.legend()

        _, ax3 = plt.subplots(figsize=(18, 5))

        total_defaults_by_month = df_full.groupby('month')['default_loans'].sum()
        df_full['default_percentage'] = (df_full['default_loans'] / total_defaults_by_month[df_full['month']].values) * 100

        for i, batch in enumerate(all_batches):
            batch_data = df_full[df_full['batch'] == batch]
            ax3.bar([p + width*i for p in x], batch_data['default_percentage'], width, label=f'Batch {batch}')

        ax3.set_xlabel('Month')
        ax3.set_ylabel('Default Percentage (%)')
        ax3.set_title('Default Percentage by Month and Batch')
        ax3.set_xticks([p + width*(len(all_batches)/2 - 0.5) for p in x])
        ax3.set_xticklabels(all_months, rotation=90)
        ax3.legend()

        plt.tight_layout()
        plt.show()


    def plot_pie_chart(self, data):
        realized_profit = float(data[0] + data[1])
        loss = float(data[2])

        labels = ['Lucro Real', 'Prejuízo']
        sizes = [realized_profit, loss]
        colors = ['tab:green', 'tab:red']
        explode = (0.1, 0)

        _, ax1 = plt.subplots()
        wedges, _, _ = ax1.pie(sizes, explode=explode, colors=colors, autopct='%1.1f%%',
                                        shadow=True, startangle=90)
        ax1.axis('equal')

        angle_realized = (wedges[0].theta2 - wedges[0].theta1) / 2. + wedges[0].theta1
        y_realized = wedges[0].r * 0.75 * np.sin(np.deg2rad(angle_realized))
        x_realized = wedges[0].r * 0.75 * np.cos(np.deg2rad(angle_realized))
        ax1.annotate(f"${sizes[0]:,.2f}", xy=(x_realized, y_realized - 0.1), ha="right", color="black")

        angle_loss = (wedges[1].theta2 - wedges[1].theta1) / 2. + wedges[1].theta1
        y_loss = wedges[1].r * 0.75 * np.sin(np.deg2rad(angle_loss))
        x_loss = wedges[1].r * 0.75 * np.cos(np.deg2rad(angle_loss))
        ax1.annotate(f"${sizes[1]:,.2f}", xy=(x_loss, y_loss + 0.1), ha="left", color="black")

        plt.title('Distribution of Realized Profit and Loss')
        plt.legend(labels, loc="upper left")
        plt.show()


    def plot_bar_chart(self, data, overall_default_rate):
        realized_profit = float(data[0] + data[1])
        loss = float(data[2])
        real_profit = realized_profit - loss

        expected_profit = float(data[3]) - (float(data[3]) * float(overall_default_rate))
        expected_loss = float(data[3]) * float(overall_default_rate)
        expected_result = expected_profit - expected_loss

        labels = ['Realized Profit', 'Loss', 'Net Profit', 'Expected Profit', 'Expected Loss', 'Expected Result']
        values = [realized_profit, loss, real_profit, expected_profit, expected_loss, expected_result]
        colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:gray']

        _, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(labels, values, color=colors)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'${yval:,.2f}', ha='center', va='bottom', fontsize=8)

        ax.set_ylabel('Amount ($)')
        ax.set_title('Total Profit and Loss')

        plt.tight_layout()
        plt.show()

    def plot_real_profit_trend(self, data):
        df = pd.DataFrame(data, columns=['month', 'realized_profit_paid', 'realized_profit_ongoing', 'loss'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        df.sort_index(inplace=True)

        df['realized_profit'] = df['realized_profit_paid'] + df['realized_profit_ongoing']
        df['real_profit'] = df['realized_profit'] - df['loss']

        df['real_profit_millions'] = df['real_profit'] / 1e6
        df['loss_millions'] = df['loss'] / 1e6

        _, ax = plt.subplots(figsize=(18, 10))
        width = 0.35
        x = np.arange(len(df.index))

        bars1 = ax.bar(x - width/2, df['real_profit_millions'], width, label='Lucro Real', color='tab:green')
        bars2 = ax.bar(x + width/2, df['loss_millions'], width, label='Prejuízo', color='tab:red')

        for bar in bars1:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'${yval:,.2f}M', ha='center', va='bottom', fontsize=8)

        for bar in bars2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'${yval:,.2f}M', ha='center', va='bottom', fontsize=8)

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($ millions)')
        ax.set_title('Real Profit and Loss Evolution')
        ax.set_xticks(x)
        ax.set_xticklabels(df.index.strftime('%Y-%m'), rotation=90)
        ax.legend()

        plt.tight_layout()
        plt.show()


    def plot_profit_table(self, data):
        df = pd.DataFrame(data, columns=['month', 'realized_profit_paid', 'realized_profit_ongoing', 'loss'])
        df['month'] = pd.to_datetime(df['month'])
        df.set_index('month', inplace=True)

        df.sort_index(inplace=True)

        df['realized_profit'] = df['realized_profit_paid'] + df['realized_profit_ongoing']
        df['real_profit'] = df['realized_profit'] - df['loss']

        table_data = df[['real_profit', 'loss']].copy()
        table_data.columns = ['Real Profit ($)', 'Loss ($)']
        table_data.reset_index(inplace=True)
        table_data['month'] = table_data['month'].dt.strftime('%Y-%m')

        table_data['Real Profit ($)'] = table_data['Real Profit ($)'].apply(lambda x: f"${x:,.2f}")
        table_data['Loss ($)'] = table_data['Loss ($)'].apply(lambda x: f"${x:,.2f}")

        display(table_data)