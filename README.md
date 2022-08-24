# Sam Media challenge
Welcome to the Sam Media challenge! First I would like to thank you for the time you are going to spend solving this challenge, we really appreciate your effort.

The idea of this challenge is to test your ability to work with data and extract insights from it.
If something is not clear on the description please ask us, or just take any assumption that you consider and work accordingly to these assumptions.

## Context of the challenge
Let's start describing a bit the business we work on. 
Sam media is a digital services provider. We have digital services like videos, games or virtual reality experiences, to mention a few.

We advertise our services using affiliates. Affiliates are companies that send internet traffic (people) to our services. Once the users get
to our service, they can subscribe to it. When users subscribes to our services, they are allowed to access the content of this 
service. Users will be billed (charged) on a period basis (subscription) using their phone account.

As there are a lot of digital services companies that are similar to Sam Media, aggregator companies are needed. These aggregator companies connect directly
with the phone operator and allow billing the users that are subscribed to different products from different digital services companies. 

## Tables description
#### users:
This table contains all the users that have been subscribed on the month of June on a specific country. Every row is a different user:
* **user_id**: unique user identifier
* **subscription_date**: starting date of subscription
* **unsubscription_date**: finishing date of subscription (Null means the user has not unsubscribed)
* **phone_operator**: company/operator that provides the service
* **os_name**: operative system of the user browser device
* **os_version**: version of this operating system
* **affiliate**: affiliate that sent the user to our service
* **service**: product that the user subscribed to
* **aggregator**: aggregator company that provide us the connection to the mobile phone provider(operator)

#### transactions:
This table contains all the transactions (billing attempts) that happened on the month of June on the same specific country
as user table. Remember this is a subscription service so same user can have several transactions in a month:
* **user_id**: unique user identifier
* **transaction_timestamp**: timestamp of the transaction
* **service**: product that the user subscribed to
* **phone_operator**: company/operator that provides the service
* **status**: Status of the transaction
  * Failed: Transaction failed, no amount was billed to the user
  * Pending: Transaction is pending, from this state the transaction can move to Delivered or Failed
  * Delivered: Transaction delivered. the `pricepoint` amount was charged to the user
* **pricepoint**: Amount tried to be billed to our subscriber

## The challenge

We would like you to come up with a report of our current situation in this country. 

To extract the insights for this report you must use python. Please use python for the data loading,
cleaning and/or aggregation. Would be nice if you can support this report with some graphs. For this, please use any tool 
you are familiar with (excel also works ;) )

As we also like to test your python and code development skills there are a few more constraints:

- **Create a git repository**.
- **Use python3+** when handling data (visualization tool is up to you!).
- **Create a virtual environment** for this project (please exclude anaconda). You can use any python package you need but please push to the repo just the `requirements.txt`
- Use Classes whenever possible (for example, having the data cleaning code under a class & methods), **at least create one Class**. It is not recommended the use of jupyter notebooks as they don't work well with classes.

## Final thoughts
Lastly please remember that we will evaluate your skills using python and extracting insights from the raw data so things 
like comments, readability and cleanliness of the code is appreciated.

Do not write too much text! Just the necessary to help you later on during your presentation to our data team members.
During this presentation you will have time to explain better why you did what you did. 

Good luck!!

Sam Media Data team