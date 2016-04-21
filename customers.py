"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    # TODO: need to implement this


    def __init__(self, first_name, last_name, email, pw):
        """Initialize customer"""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.pw = pw

    def __repr__(self):
        """Prints customer information"""
        return "Customer: {} {}, email address: {}, password: {}".format(self.first_name, 
                                                                        self.last_name, 
                                                                        self.email, 
                                                                        self.pw)


def read_customers_from_file(filepath):
    """Read customers from a text file"""

    customers = open(filepath)

    customer_database = {}

    for customer in customers:
        customer = customer.strip()
        customer = customer.split("|")
        first_name, last_name, email, pw = customer


        customer_database[email] = Customer(first_name, last_name, email, pw)

    return customer_database


def get_by_email(email):
    """Get a customer by email address"""

    return customers[email]



customers = read_customers_from_file('customers.txt')

# print customers