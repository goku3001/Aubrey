import datetime
from dateutil.relativedelta import relativedelta

### VARIABLES GIVEN
policy_info = [{				# A list of dictionaries
	'total_financable': 10000, 
	'policy_effective_date': datetime.date(2015, 1, 1),
	'policy_term': 'Annual',
	'prorata': True,
	'policy_days_to_cancel': 5,
	'minimum_earned_premium': 25}]#,
	#{...}, ...]
	# values for policy_term will either be 'annual' (365 days most years) or
		# a datetime.date object.

quote_info = {
	'equity_required': 5,	# as in 5%. Could be zero or negative
	'apr': 5,				# also as in 5%.
	'state_days_to_cxl': 15,
	'payment_period': 'Monthly'} # will equal 'Monthly', 'Quarterly', or 'Semiannually'

equity_required = 5		# This is a percent of the total_financable.
installment_range = [7, 11] # The answer returned must satisfy
							# 7 <= number_of_payments <= 11
first_pay_date_range = [25, 60] # The first payment must be at least 25 days
								# after the earliest policy_effective_date,
								# and not more than 60 days after it


### A QUICK, POSSIBLY INCOMPLETE EXPLANATION OF THE PROBLEM ###

# The goal is to find the combination of a down_payment_percent, 
	# number_of_payments, and first_due_date that ends up yielding the
	# highest amount of interest paid while maintining an equity position
	# greater than or equal to a given level (as a % of total_financable).
# Your function should take in the variables above, then return the optimal
	# down_payment_percent, number_of_payments, and first_due_date.


def return_optimal_payment_terms(policy_info, quote_info, equity_required, 
	installment_range, first_pay_date_range):
	### things happen...
	return down_payment_percent, number_of_payments, first_due_date

# equity_percentage = ((unearned_premium + amount_paid) / \
	# sum_of_total_financable) - 1
# unearned_premium = total_financable - earned_premium
# earned_premium = max(days_policy_in_effect / length_of_policy, \
	# total_financable * (1 - minimum_earned_premium)) * short_rate_penalty
# if prorata == True, short_rate_penalty = 1. else: short_rate_penalty = .9
# length_of_policy comes from find_length_of_policy() below
# days_policy_in_effect = max(due_date_of_cancellation - \
	# policy_effective_date, 0) 
	### It could to be negative if one policy is effective far after another.
	### But finance companies don't pay for policies until after the effective
	### date, so a policy like that should drop out of the equation. Hence the max()
# due_date_of_cancellation comes from get_cancellation_dates(), which
	# can be called after return_payment_dates(), which requires guesses
	# about the first_due_date and num_of_install

def get_sum_of_total_financable(policy_info):
	sum = 0.0
	for policy in policy_info:
		sum += policy.total_financable
	return sum
# amount_paid = sum_of_total_financable * down_payment_percent + \
	# installments_paid * payment_amount

	# int_rate_dict = {'buy_rate': quote_info['apr']}
def get_loan_amt_dict(policy_info, down_payment_percent):
	"""Return a list of dictionaries for finance_formulas. \
		get_payment_fin_charge_total_of_pay_apr_buy_rate"""
	loan_amt_dict = []
	for policy in policy_info:
		loan_amt_dict += {'loan_amt': policy.total_financable * (
			1 - down_payment_percent), 'date': policy.policy_effective_date}
	return loan_amt_dict

# payment_amount, finance_charge_dict, unimportant_var, precise_apr = \
	# finance_formulas.get_payment_fin_charge_total_of_pay_apr_buy_rate(
	# loan_amt_dict, number_of_payments, int_rate_dict, payment_period, 
	# first_due_date)

def find_length_of_policy(policy_effective_date, policy_term):
	"""Return the number of days a policy is in effect as a float"""
	if policy_term == 'Annual':
		# Find out of the year has 365 or 366 days
		policy_expiration_date = policy_effective_date + relativedelta(years=1)
		datetime_length = policy_expiration_date - policy_effective_date
	else:
		# If policy_term isn't 'Annual', then it should be a datetime object
		datetime_length = policy_term - policy_effective_date

	# Convert from a datetime.date object to a float
	return (datetime_length / datetime.timedelta(1))


# first_due_date and num_of_install are potential solutions to the general problem
def return_payment_dates(payment_period, num_of_install, first_due_date):
	"""Return a list of datetime.date objects representing payment dates.
		The list is ordered from first to last"""
		### Assumes the first_due_date is not on a weekend!
	payment_dates = []
	
	if payment_period == 'Monthly':
		additional_pays = 1
	elif payment_period == 'Quarterly':
		additional_pays = 3
	elif payment_period == 'Semi-annually':
		additional_pays = 6
	else:
		raise ValueError("There was an error processing this payment schedule")
	
	for item in range(num_of_install):
		if item == 0:
			payment_dates += [first_due_date]
		else:
			## Change due dates from Sat/Sun to Monday
			test_date = first_due_date + \
				relativedelta(months = item * additional_pays)
			if datetime.date.weekday(test_date) == 5: # Saturday
				payment_dates += [first_due_date + relativedelta(
					months = item * additional_pays, days = 2)]
			elif datetime.date.weekday(test_date) == 6: # Sunday
				payment_dates += [first_due_date + relativedelta(
					months = item * additional_pays, days = 1)]
			else:	
				payment_dates += [first_due_date + \
					relativedelta(months = item * additional_pays)]

	return payment_dates


def get_cancellation_dates(payment_dates, state_days_to_cancel, 
	policy_days_to_cancel):
	"""Given a list of payment due dates, return a list of potential
		cancellation dates, ordered from earliest to latest"""
	cancellation_dates = []
	
	for payment in payment_dates:
		cxl_date = payment + datetime.timedelta(days_to_cancel)
		if datetime.date.weekday(cxl_date) == 5: # Saturday
			cxl_date = cxl_date + datetime.timedelta(2)
		elif datetime.date.weekday(cxl_date) == 6: # Sunday
			cxl_date = cxl_date + datetime.timedelta(1)
		cancellation_dates += [cxl_date]
	
	return cancellation_dates

class account(object):
    def __init__(self, total_financiable, payment_period, num_of_install, first_due_date, down_payment_percent, days_to_cancel, **kwargs):
        self.payment_period = payment_period
        self.num_of_install = num_of_install
        self.first_due_date = first_due_date
        self.down_payment_percent = down_payment_percent
        self.days_to_cancel = days_to_cancel
        self.total_financiable = total_financiable


    def getTotalFinanciable(self):
        return self.total_financiable
        
    def getPaymentPeriod(self):
        return self.payment_period

    def getNumberInstallments(self):
        return self.num_of_install

    def getFirstDueDate(self):
        if datetime.date.weekday(self.first_due_date) in [5,6]:
            assert ValueError("The first due date is on a weekend")
        else:
            return self.first_due_date

    def getDownPaymentPercent(self):
        return self.down_payment_percent

    def getDaysToCancel(self):
        return self.days_to_cancel

    def getPaymentDates(self):
            """Return a list of datetime.date objects representing payment dates.
                    The list is ordered from first to last"""
                    ### Assumes the first_due_date is not on a weekend!
            payment_dates = []
            payment_period = self.getPaymentPeriod()
            if payment_period == 'Monthly':
                    additional_pays = 1
            elif payment_period == 'Quarterly':
                    additional_pays = 3
            elif payment_period == 'Semi-annually':
                    additional_pays = 6
            else:
                    raise ValueError("There was an error processing this payment schedule")
            num_of_install = self.getNumberInstallments()
            first_due_date = self.getFirstDueDate()
            
            for item in range(num_of_install):
                    if item == 0:
                            payment_dates += [first_due_date]
                    else:
                            ## Change due dates from Sat/Sun to Monday
                            test_date = first_due_date + \
                                    relativedelta(months = item * additional_pays)
                            if datetime.date.weekday(test_date) == 5: # Saturday
                                    payment_dates += [first_due_date + relativedelta(
                                            months = item * additional_pays, days = 2)]
                            elif datetime.date.weekday(test_date) == 6: # Sunday
                                    payment_dates += [first_due_date + relativedelta(
                                            months = item * additional_pays, days = 1)]
                            else:	
                                    payment_dates += [first_due_date + \
                                            relativedelta(months = item * additional_pays)]

            return payment_dates

    def getCancellationDates(self):
            """Given a list of payment due dates, return a list of potential
                    cancellation dates, ordered from earliest to latest"""
            cancellation_dates = []
            
            for payment in self.getPaymentDates():
                    cxl_date = payment + datetime.timedelta(self.getDaysToCancel())
                    if datetime.date.weekday(cxl_date) == 5: # Saturday
                            cxl_date = cxl_date + datetime.timedelta(2)
                    elif datetime.date.weekday(cxl_date) == 6: # Sunday
                            cxl_date = cxl_date + datetime.timedelta(1)
                    cancellation_dates += [cxl_date]
            
            return cancellation_dates

a = account("Monthly", 10000, 12, datetime.date(2015, 1, 1), .12, 45, extraVar = "extra")

