"""
AccountDashboard Extension
"""

from q2_sdk.core.http_handlers.tecton_server_handler import Q2TectonServerRequestHandler
from q2_sdk.hq.hq_api.q2_api import GetAccountHistoryById
# from q2_sdk.hq.models.db_config.db_config import DbConfig
# from q2_sdk.hq.models.db_config.db_config_list import DbConfigList
# from q2_sdk.hq.models.db_config.db_env_config import DbEnvConfig, EnvValue

from .install.db_plan import DbPlan


class AccountDashboardHandler(Q2TectonServerRequestHandler):

    ## REQUIRED_CONFIGURATIONS is a dictionary of key value pairs that are necessary
    ## for the extension to run. If set, ensures the entries are set in the
    ## extension's settings file or the web server will not start.
    ## Keys are names and values are defaults written into the settings file.
    ## To override the defaults, generate the config (`q2 generate_config`) and
    ## then alter the resulting file

    # REQUIRED_CONFIGURATIONS = {
    #    # 'CONFIG1': 'Default',
    #    # 'CONFIG2': 'Default',
    # }

    # # Behaves the same way as REQUIRED_CONFIGURATIONS, but will not stop the web server
    # # from starting if omitted from the extension's settings file
    # OPTIONAL_CONFIGURATIONS = {}

    # # Behaves in a similar manner to REQUIRED_CONFIGURATIONS,
    # # but stores the data in the database instead of the settings file. Will be
    # # written into the database on `q2 install`
    # WEDGE_ADDRESS_CONFIGS = DbConfigList([
    #     # same default for all environments
    #     DbConfig('enableOptionalLogic', False),
    #
    #     # different defaults for each environment
    #     DbEnvConfig('apiUrl', EnvValue(
    #         dev='https://dev.my-domain.com',
    #         stg='https://stage.my-domain.com',
    #         prod='https://my-domain.com'
    #     ))
    # ])

    # Set this to True if you want to change which Core is configured based on database configuration
    DYNAMIC_CORE_SELECTION = False

    # Set this True if you want your extension to be available to unauthenticated users
    # IS_UNAUTHENTICATED = False

    DB_PLAN = DbPlan()

    FRIENDLY_NAME = 'AccountDashboard'  # this will be used for end user facing references to this extension like Central and Menu items.
    DEFAULT_MENU_ICON = 'landing-page'  # this will be the default icon used if extension placed at top level (not used if a child element)

    CONFIG_FILE_NAME = 'AccountDashboard'  # configuration/AccountDashboard.py file must exist if REQUIRED_CONFIGURATIONS exist

    TECTON_URL = 'https://cdn1.onlineaccess1.com/cdn/base/tecton/v1.31.0/q2-tecton-sdk.js'

    def __init__(self, application, request, **kwargs):
        """
        If you need variables visible through the lifetime of this request,
        feel free to add them in this function
        """
        super().__init__(application, request, **kwargs)
        # self.variable_example = 12345

    # # Uncomment this to allow the IDE to give you better hinting on a specific core (Symitar in this example)
    # from q2_cores.Symitar.core import Core as SymitarCore
    # @property
    # def core(self) -> SymitarCore:

    #     # noinspection PyTypeChecker
    #     return super().core

    @property
    def router(self):
        """
        Your extension's routing map. To handle a request, a method must be listed here. When a POST request is
        made to this extension with a routing_key value, the extension will route the request to the method linked
        to that key. The methods referenced here are defined below.
        """
        router = super().router
        router.update({
            'default': self.default,
            'submit': self.submit,
            # Add new routes here
        })

        return router

    def get(self, *args, **kwargs):
        """
        Most Q2 extensions will be handling POSTs from the Online component, but
        GET requests can also be handled here. If you delete this function, GET
        will simply not be a supported Verb for this extension.
        PUT, DELETE, etc can also be handled by creating an appropriately named
        function. This is based off of Tornado's request handling.
        More info at http://www.tornadoweb.org/en/stable/guide/structure.html?highlight=post#subclassing-requesthandler
        """
        self.write("Hello World GET: From AccountDashboard")

    async def default(self):
        account_models = []
        for account in self.account_list:
            account_models.append({
                'account_num': account.host_acct_id,
                'account_name': account.product_name,
                'account_balance': account.balance_to_display
            })

        template = self.get_template('index.html.jinja2', {
            'accounts': account_models
        })

        html = self.get_tecton_form(
            "AccountDashboard",
            custom_template=template,
            routing_key="submit"
        )
        return html

    async def submit(self):
        params_obj = GetAccountHistoryById.ParamsObj(
            self.logger,
            self.form_fields['account_id'],
            '',
            hq_credentials=self.hq_credentials
        )

        hq_response = await GetAccountHistoryById.execute(params_obj)

        transaction_models = []

        for transaction in hq_response.result_node.Data.AllHostTransactions.Transactions:
            display_date = str(transaction.PostDate)
            display_amount = str(transaction.TxnAmount)
            is_credit = (transaction.SignedTxnAmount > 0)
            display_description = str(transaction.Description)

            transaction_models.append({
                'display_date': display_date,
                'display_amount': display_amount,
                'is_credit': is_credit,
                'display_description': display_description
            })

        template = self.get_template(
            'transaction_history.html.jinja2', {
                'header': "Transaction History",
                'transactions': transaction_models,
                'current_account_id': self.form_fields['account_id'],
            }
        )

        html = self.get_tecton_form(
            "Transaction History",
            custom_template=template,
            hide_submit_button=True
        )

        return html
