# First let's set the default settings:
from q2_sdk.core.default_settings import *

# To override any defaults, simply redefine them below.
# Some commonly overridden values are commented out below

# INSTALLED_EXTENSIONS does NOT mean installed in the database, but rather registered to run
# within this server.
# Can be a list of strings, a list of tuple's or a combination of both.
# Tuple format is ('short_name', 'path_to_module')
# Example:
# INSTALLED_EXTENSIONS = [
#   'extension_1'
#   ('extension_2', 'sub_dir.extension_2')
# ]
#
INSTALLED_EXTENSIONS = [
    # "your_extension_here"
]

#Set this to true to pull hq credentials only from vault or another source, never from environment
MULTITENANT = False

# If you make a custom core (q2 create_coreflow), add the path here
# to be discoverable for use with DYNAMIC_CORE_SELECTION
#CUSTOM_CORES = {
#    'CoreName': 'module_path_that_contains_Core_object',
#    'FooCore': 'FooCore.extension'
#}

# Uncomment this line to define your own logging.conf location
# LOGGING_CONF = os.path.abspath('./logging.conf')

# An example of how to add logging filters that will affect every extension
# from q2_sdk.core.q2_logging import filters
# GLOBAL_LOGGING_FILTERS.append(filters.TaxIDFilter)

CORE = None
# CORE CONNECTIVITY
# Core calls are OFF by default. To enable, uncomment the 'CORE =' line below
# If DEBUG is set to True above, Core responses will be mocked
# If DEBUG is set to False above, Core calls will call AdapterPassThru from hq_api
# Replace the line below with a reference to a module in q2_cores or a key from the CUSTOM_CORES dict above
#     - This can either be a core that comes with the q2_cores package or one that you write yourself
#     - Example below show how to import the Symitar core

# CORE = 'Symitar'

IS_CUSTOMER_CREATED = True
COMPANY = 'LoanPro'

# Q2 blocks all outbound traffic in our datacenter by default.
# To enable a url through our firewall, a networking request must be made
# through Salesforce. If you are an SDK client, the Q2 SDK team can handle this
# on your behalf by sending an email to sdk@q2ebanking.com.
# This python list is merely a convenient way to encourage us to remember.
# Unless a url is added to this list, it will be blocked (in DEBUG mode).
OUTBOUND_WHITELIST.extend(['localhost'])

# There are a handful of functions in the SDK that can be dangerous
# if used improperly. To avoid accidents, you need to opt in to
# their usage. This will become apparent if you try to use one.
DANGEROUS_WHITELIST = []

# Only respected in dev. If defined, will override asset urls per extension.
ASSET_URL_OVERRIDE = {
    # 'extension_1': 'http://localhost:3000',
    # 'extension_2': 'http://localhost:3001',
}
VAULT_SCOPED_READ = True
