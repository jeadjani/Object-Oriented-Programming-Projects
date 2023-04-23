import math

from argparse import ArgumentParser
import math
import sys


def parse_args(arglist):
    """Parse and validate command-line arguments.
    
    This function expects the following required arguments, in this order:
    
        mortgage_amount (float): total amount of a mortgage
        annual_interest_rate (float): the annual interest rate as a value
            between 0 and 1 (e.g., 0.035 == 3.5%)
        
    This function also allows the following optional arguments:
    
        -y / --years (int): the term of the mortgage in years (default is 30)
        -n / --num_annual_payments (int): the number of annual payments
            (default is 12)
        -p / --target_payment (float): the amount the user wants to pay per
            payment (default is the minimum payment)
    
    Args:
        arglist (list of str): list of command-line arguments.
    
    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)
    
    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")
    
    return args




def get_min_payment(principal, arp, term=30, payments=12):
    """ Solves for the minimum mortgage payment and raises the value 
    to the next highest integer
    
    Args:
        principal: the total amount of the mortgage.
        arp: the annual interest rate.
        term: the mortgage legth in years.
        payments: the number of payments per year. 
   
    Returns:
        value for the minimum payment to the next highest integer
    """
    nn=term*payments
    r=arp/payments
    A=(principal*r*(1+r)**nn)/((1+r)**nn -1)
    minpayment=math.ceil(A)
    return minpayment

def interest_due(balance, arp, payments=12):
    """Solves for the amount of interest due
    
    Args:
        balance: the part of the principal that hasn't been paid yet
        arp: the annual interest rate.
        payments: the number of payments per year.
    
    Returns:
        the amount of interest due in the next payment
    """
    i= int(balance*(arp/payments))
    return i
    
def remaining_payments(balance, arp, target, payments=12):
    """Counts the remaining number of payments left to pay off the mortgage
    
    Args:
        balance: the part of the principal that hasn't been paid yet
        arp: the annual interest rate.
        target: the amount that the user wants to pay
        payments: the number of payments per year.
        
    Returns:
        the number of payments required to pay off the mortgage
    """
    no_of_payments=0
    while balance > 0:
        balance-=target-(interest_due(balance,arp,payments))
        no_of_payments+=1
    return no_of_payments
    
    
def main(principal, arp, term=30, payments=12, target= None):
    """Solves and displays the target payment and the total payments
    
    Args:
        principal: the total amount of the mortgage.
        arp: the annual interest rate.
        term: the mortgage length in years.
        payments: the number of payments per year.
        target: the amount that the user wants to pay
        
    Returns:
        the target payment and the total payments for the user
    """
    
    print(get_min_payment(principal,arp,term,payments))
    if target is None:
        target=get_min_payment(principal,arp,term,payments)
        if target < get_min_payment(principal,arp,term,payments):
            print("Your target is less than the minimum payment for this mortgage")
        else:
            ttp=remaining_payments(principal,arp,target,payments)
            print(f"If you make payments of {target}, you will pay off the mortgage in {ttp} payments")
            
    
    pass
    """
    
    if target == 0:
        raise get_min_payment(principal,arp,term,payments)
            with target < minpayment:
                print("Your target payment is less than the minimum payment for this mortgage")
    else:
        raise remaining_payments(balance, arp, target, payments) 
    """


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)
