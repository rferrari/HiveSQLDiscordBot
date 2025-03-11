from dotenv import load_dotenv
import os

load_dotenv()

DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() == "true"

# Discord Configuration
DISCORD_CONFIG = {
    "token": os.environ.get("DISCORD_TOKEN"),
    "admin_id": os.environ.get("DISCORD_ADMIN_ID"),
    "cool_down_duration": 2,
    "max_daily_queries": 25
}

# Database Configuration
DB_CONFIG = {
    "server": os.environ.get("HIVESQL_SERVER"),
    "database": os.environ.get("HIVESQL_DATABASE"),
    "user": os.environ.get("HIVESQL_USER"),
    "password": os.environ.get("HIVESQL_PWD")
}

# LLM Configuration
LLM_CONFIG = {
    "groq_api_key": os.environ.get("GROQ_API_KEY", False),
    "openai_api_key": os.environ.get("OPENAI_API_KEY", False),
    "groq_model": os.environ.get("GROQ_LLM_MODEL", "gemma2-9b-it"),
    "openai_model": os.environ.get("OPENAI_LLM_MODEL", "gpt-4o-mini"),
    "eval_temp": float(os.environ.get("EVAL_TEMPERATURE", 0.7)),
    "query_temp": float(os.environ.get("QUERY_TEMPERATURE", 0.1)),
    "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", 1024))
}

# SQL Queries
SQL_QUERIES = {
    "select_tables": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS;",
    
    "create_tables_schema": """
    SELECT 
        'CREATE TABLE ' + '' + TABLE_NAME + ' (' +
        STRING_AGG(COLUMN_NAME, ', ') + ');' AS CreateTableDDL
    FROM INFORMATION_SCHEMA.COLUMNS
    GROUP BY TABLE_SCHEMA, TABLE_NAME;
    """,

    "create_tables_schema_full": """
    SELECT 
    'CREATE TABLE ' +TABLE_NAME + ' (' + 
    STRING_AGG(COLUMN_NAME + ' ' + DATA_TYPE + 
        COALESCE('(' + CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR) + ')', ''), ', ') 
    + ');' AS CreateTableDDL
    FROM INFORMATION_SCHEMA.COLUMNS
    GROUP BY TABLE_SCHEMA, TABLE_NAME;
    """
}

SKIP_TABLES = [
    # "Reblogs",
    # "TxEscrowApproves",
    # "TxProposalVoteUpdates",
    # "TxEscrowDisputes",
    # "VOHardforks",
    # "TxEscrowReleases",
    "TxEscrowTransfers",
    # "TxFeeds",
    # "TxPows",
    # "TxVotes",
    # "VOLimitOrderCancelleds",
    # "TxWithdraws",
    # "Communities",
    # "VOExpiredAccountNotifications",
    # "TxWithdrawVestingRoutes",
    # "TxWitnessUpdates",
    # "TxAccountCreates",
    # "VOFillCollateralizedConvertRequests",
    # "Witnesses",
    # "VOPowRewards",
    "VOFillRecurrentTransfers",
    # "VOEscrowApproveds",
    # "CommunitiesSubscribers",
    # "CommunitiesRoles",
    # "ProposalsApprovals",
    # "Delegations",
    # "VOHardforkHives",
    # "Proposals",
    "VOTransferToVestingCompleteds",
    # "VOProposalFees",
    # "DynamicGlobalProperties",
    # "Tags",
    # "TxAccountRecoveryConfirms",
    # "Comments",
    # "TxTransfers",
    # "VOAuthorRewards",
    # "Blacklists",
    # "TxProposalUpdates",
    # "VOClearNullAccountBalances",
    # "BlacklistsFollows",
    # "VOCommentBenefactorRewards",
    # "TxAccountRecoveryChanges",
    # "TxAccountRecoveryRequests",
    # "Mutes",
    # "VOCollateralizedConvertImmediateConversions",
    # "VOCurationRewards",
    # "MutesFollows",
    # "VOFillConvertRequests",
    # "TxLimitOrdersCreates",
    # "TxLimitOrdersCancels",
    # "VOFillOrders",
    "VOFillTransferFromSavings",
    # "VOSPSConverts",
    # "RCDelegations",
    # "VOFillVestingWithdraws",
    # "TxAccountUpdates2",
    # "TxProposalRemoves",
    # "VOInterests",
    # "VOLiquidityRewards",
    # "VOProposalPays",
    # "VODHFConversions",
    # "VOCommentPayoutUpdates",
    # "VOProducerRewards",
    # "VOHardforkHiveRestores",
    # "VOReturnVestingDelegations",
    # "VOSPSFunds",
    # "VOShutdownWitnesses",
    # "TxCollateralizedConverts",
    # "VOCommentRewards",
    "TxRecurrentTransfers",
    # "VODelayedVotings",
    # "Transactions",
    # "Blocks",
    # "Accounts",
    # "TxDeclineVotingRights",
    # "TxDelegateVestingShares",
    # "TxDeleteComments",
    # "TxAccountUpdates",
    # "TxAccountWitnessProxies",
    # "VOEscrowRejecteds",
    # "TxAccountWitnessVotes",
    # "TxClaimRewardBalances",
    # "VODHFFundings",
    # "VOAccountCreateds",
    # "TxComments",
    # "Followers",
    # "TxCommentsOptions",
    # "TxAccountClaims",
    # "TxConverts",
    # "TxProposalCreates",
    # "TxWitnessSetProperties",
    # "TxCustoms",
    # "VOChangedRecoveryAccounts"
]
