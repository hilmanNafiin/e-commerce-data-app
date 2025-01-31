class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_daily_orders_df(self):
        daily_orders_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_orders_df = daily_orders_df.reset_index()
        daily_orders_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "revenue"
        }, inplace=True)
        return daily_orders_df
    
    def create_sum_spend_df(self):
        sum_spend_df = self.df.resample(rule='D', on='order_approved_at').agg({
            "payment_value": "sum"
        })
        sum_spend_df = sum_spend_df.reset_index()
        sum_spend_df.rename(columns={
            "payment_value": "total_spend"
        }, inplace=True)
        return sum_spend_df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='product_count', ascending=False)
        return sum_order_items_df

    def review_score_df(self):
        review_scores = self.df['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()
        return review_scores, most_common_score

    def create_bystate_df(self):
        bystate_df = self.df.groupby(by="customer_state").customer_id.nunique().reset_index()
        bystate_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(), 'customer_state']
        bystate_df = bystate_df.sort_values(by='customer_count', ascending=False)
        return bystate_df, most_common_state

    def create_order_status(self):
        order_status_df = self.df["order_status"].value_counts().sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()
        return order_status_df, most_common_status

    def create_monthly_orders_df(self):
        monthly_orders_df = self.df.resample(rule='M', on='order_approved_at').agg({
            "order_id": "nunique"
        })
        monthly_orders_df = monthly_orders_df.reset_index()
        monthly_orders_df.rename(columns={
            "order_id": "order_count"
        }, inplace=True)
        return monthly_orders_df

    def create_monthly_spend_df(self):
        monthly_spend_df = self.df.resample(rule='M', on='order_approved_at').agg({
            "payment_value": "sum"
        })
        monthly_spend_df = monthly_spend_df.reset_index()
        monthly_spend_df.rename(columns={
            "payment_value": "total_spend"
        }, inplace=True)
        return monthly_spend_df

    def create_bycity_df(self):
        bycity_df = self.df.groupby(by="customer_city").customer_id.nunique().reset_index()
        bycity_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        bycity_df = bycity_df.sort_values(by='customer_count', ascending=False)
        return bycity_df

    def create_review_distribution_df(self):
        review_distribution = self.df['review_score'].value_counts(normalize=True) * 100
        return review_distribution
    
class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        brazil = self.mpimg.imread(self.urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='maroon')
        self.plt.axis('off')
        self.plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
        self.st.pyplot()