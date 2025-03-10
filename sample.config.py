from dotenv import load_dotenv
import os

load_dotenv()

# Discord Configuration
DISCORD_CONFIG = {
    "token": os.environ.get("DISCORD_TOKEN"),
    "admin_id": os.environ.get("DISCORD_ADMIN_ID")
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
    "groq_api_key": False,#os.environ.get("GROQ_API_KEY"),
    "openai_api_key": os.environ.get("OPENAI_API_KEY"),
    "model": os.environ.get("LLM_MODEL"),
    "temperature": float(os.environ.get("LLM_TEMPERATURE", 0.7)),
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
    # "Blocks",
    # "TxAccountClaims",
    # "TxAccountCreates",
    # "TxAccountRecoveryChanges",
    # "TxAccountRecoveryConfirms",
    # "TxAccountRecoveryRequests",
    # "TxCollateralizedConverts",
    # "TxCustoms",
    # "TxDeclineVotingRights",
    # "TxDeleteComments",
    # "TxEscrowApproves",
    # "TxEscrowDisputes",
    # "TxEscrowReleases",
    # "TxEscrowTransfers",
    # "TxFeeds",
    # "TxLimitOrdersCancels",
    # "TxLimitOrdersCreates",
    # "TxPows",
    # "TxProposalCreates",
    # "TxProposalRemoves",
    # "TxProposalUpdates",
    # "TxRecurrentTransfers",
    # "TxWitnessSetProperties",
    # "TxWitnessUpdates",
    # "VOAccountCreateds",
    # "VOChangedRecoveryAccounts",
    # "VOClearNullAccountBalances",
    # "VOCollateralizedConvertImmediateConversions",
    # "VODelayedVotings",
    # "VODHFConversions",
    # "VOEscrowApproveds",
    # "VOEscrowRejecteds",
    # "VOExpiredAccountNotifications",
    # "VOFillCollateralizedConvertRequests",
    # "VOFillConvertRequests",
    # "VOFillOrders",
    # "VOFillRecurrentTransfers",
    # "VOFillTransferFromSavings",
    # "VOFillVestingWithdraws",
    # "VOHardforkHiveRestores",
    # "VOHardforkHives",
    # "VOHardforks",
    # "VOInterests",
    # "VOLimitOrderCancelleds",
    # "VOLiquidityRewards",
    # "VOPowRewards",
    # "VOProducerRewards",
    # "VOProposalFees",
    # "VOProposalPays",
    # "VOReturnVestingDelegations",
    # "VOShutdownWitnesses",
    # "VOSPSConverts",
    # "VOSPSFunds",
    # "VOTransferToVestingCompleteds"
]




# CREATE TABLE Accounts (active, balance, balance_symbol, created, curation_rewards, delayed_votes, delegated_vesting_shares, delegated_vesting_shares_symbol, downvote_manabar_current_mana, downvote_manabar_last_update_time, governance_vote_expiration_ts, hbd_balance, hbd_balance_symbol, hbd_last_interest_payment, hbd_seconds, hbd_seconds_last_update, id, json_metadata, last_account_recovery, last_account_update, last_owner_update, last_post, last_root_post, last_vote_time, memo_key, mined, name, next_vesting_withdrawal, owner, pending_claimed_accounts, post_count, posting, posting_json_metadata, posting_rewards, proxied_vsf_votes, proxy, received_vesting_shares, received_vesting_shares_symbol, recovery_account, reputation, reputation_ui, reward_hbd_balance, reward_hbd_balance_symbol, reward_hive_balance, reward_hive_balance_symbol, reward_vesting_balance, reward_vesting_balance_symbol, reward_vesting_hive, reward_vesting_hive_symbol, savings_balance, savings_balance_symbol, savings_hbd_balance, savings_hbd_balance_symbol, savings_hbd_last_interest_payment, savings_hbd_seconds, savings_hbd_seconds_last_update, savings_withdraw_requests, to_withdraw, TS, vesting_balance, vesting_balance_symbol, vesting_shares, vesting_shares_symbol, vesting_withdraw_rate, vesting_withdraw_rate_symbol, voting_manabar_current_mana, voting_manabar_last_update_time, voting_power, withdraw_routes, withdrawn, witness_votes, witnesses_voted_for);
# CREATE TABLE Blacklists (blacklisted, blacklister);
# CREATE TABLE BlacklistsFollows (account, blacklist);
# CREATE TABLE Blocks (block_num, timestamp, witness);
# CREATE TABLE Comments (abs_rshares, active, active_votes, allow_curation_rewards, allow_votes, author, author_rewards, beneficiaries, body, body_language, body_length, cashout_time, category, children, created, curator_payout_value, depth, ID, json_metadata, last_payout, last_update, max_accepted_payout, max_cashout_time, net_rshares, net_votes, parent_author, parent_permlink, pending_payout_value, percent_hbd, permlink, promoted, reward_weight, root_title, title, total_payout_value, total_pending_payout_value, total_vote_weight, TS, url, vote_rshares);
# CREATE TABLE Communities (about, description, flag_text, language, name, nsfw, title, TS, type);
# CREATE TABLE CommunitiesRoles (account, community, role, title);
# CREATE TABLE CommunitiesSubscribers (community, subscriber);
# CREATE TABLE Delegations (delegatee, delegator, vests);
# CREATE TABLE DynamicGlobalProperties (available_account_subsidies, confidential_hbd_supply, confidential_supply, confidential_supply_symbol, content_reward_percent, current_aslot, current_hbd_supply, current_hbd_supply_symbol, current_remove_threshold, current_supply, current_supply_symbol, current_witness, delegation_return_period, downvote_pool_percent, early_voting_seconds, hbd_interest_rate, hbd_print_rate, hbd_start_percent, hbd_stop_percent, head_block_id, head_block_number, hive_per_vest, ID, init_hbd_supply, init_hbd_supply_symbol, last_budget_time, last_irreversible_block_num, max_consecutive_recurrent_transfer_failures, max_open_recurrent_transfers, max_recurrent_transfer_end_date, maximum_block_size, mid_voting_seconds, min_recurrent_transfers_recurrence, next_maintenance_time, num_pow_witnesses, participation_count, pending_rewarded_vesting_hive, pending_rewarded_vesting_hive_symbol, pending_rewarded_vesting_shares, pending_rewarded_vesting_shares_symbol, price_hbd_usd, price_hive_usd, recent_slots_filled, required_actions_partition_percent, reverse_auction_seconds, smt_creation_fee, smt_creation_fee_symbol, sps_fund_percent, sps_interval_ledger, sps_interval_ledger_symbol, target_votes_per_period, time, total_pow, total_reward_fund_hive, total_reward_fund_hive_symbol, total_reward_shares2, total_vesting_fund_hive, total_vesting_fund_hive_symbol, total_vesting_shares, total_vesting_shares_symbol, vesting_reward_percent, virtual_supply, virtual_supply_symbol, vote_power_reserve_rate);
# CREATE TABLE Followers (follower, following);
# CREATE TABLE Mutes (muted, muter);
# CREATE TABLE MutesFollows (account, mutelist);
# CREATE TABLE Proposals (creator, daily_pay, daily_pay_symbol, deleted, end_date, id, permlink, receiver, start_date, subject, total_votes);
# CREATE TABLE ProposalsApprovals (proposal_id, voter);
# CREATE TABLE RCDelegations (delegatee, delegator, rc);
# CREATE TABLE Reblogs (account, author, permlink, timestamp);
# CREATE TABLE Tags (comment_ID, tag);
# CREATE TABLE Transactions (block_num, expiration, transaction_num, tx_id, type);
# CREATE TABLE TxAccountClaims (creator, extensions, fee, ID, timestamp, tx_id);
# CREATE TABLE TxAccountCreates (active_key, creator, delegation, extensions, fee, ID, json_metadata, memo_key, new_account_name, owner_key, posting_key, timestamp, tx_id);
# CREATE TABLE TxAccountRecoveryChanges (account_to_recover, ID, new_recovery_account, timestamp, tx_id);
# CREATE TABLE TxAccountRecoveryConfirms (account_to_recover, ID, new_owner_authority, recent_owner_authority, timestamp, tx_id);
# CREATE TABLE TxAccountRecoveryRequests (account_to_recover, ID, new_owner_authority, recovery_account, timestamp, tx_id);
# CREATE TABLE TxAccountUpdates (account, active, ID, json_metadata, memo_key, owner, posting, timestamp, tx_id);
# CREATE TABLE TxAccountUpdates2 (account, active, extensions, ID, json_metadata, memo_key, owner, posting, posting_json_metadata, timestamp, tx_id);
# CREATE TABLE TxAccountWitnessProxies (account, ID, proxy, timestamp, tx_id);
# CREATE TABLE TxAccountWitnessVotes (account, approve, ID, timestamp, tx_id, witness);
# CREATE TABLE TxClaimRewardBalances (account, ID, reward_hbd, reward_hive, reward_vests, timestamp, tx_id);
# CREATE TABLE TxCollateralizedConverts (amount, amount_symbol, ID, owner, requestid, timestamp, tx_id);
# CREATE TABLE TxComments (author, body, ID, json_metadata, parent_author, parent_permlink, permlink, timestamp, title, tx_id);
# CREATE TABLE TxCommentsOptions (allow_curation_rewards, allow_votes, author, extensions, ID, max_accepted_payout, percent_hbd, permlink, timestamp, tx_id);
# CREATE TABLE TxConverts (amount, amount_symbol, ID, owner, requestid, timestamp, tx_id);
# CREATE TABLE TxCustoms (ID, json, required_auth, required_auths, required_posting_auth, required_posting_auths, tid, timestamp, tx_id);
# CREATE TABLE TxDeclineVotingRights (account, decline, ID, timestamp, tx_id);
# CREATE TABLE TxDelegateVestingShares (delegatee, delegator, ID, timestamp, tx_id, vesting_shares);
# CREATE TABLE TxDeleteComments (author, ID, permlink, timestamp, tx_id);
# CREATE TABLE TxEscrowApproves (agent, approve, escrow_id, from, ID, timestamp, to, tx_id, who);
# CREATE TABLE TxEscrowDisputes (agent, escrow_id, from, ID, timestamp, to, tx_id, who);
# CREATE TABLE TxEscrowReleases (agent, escrow_id, from, hbd_amount, hive_amount, ID, receiver, timestamp, to, tx_id, who);
# CREATE TABLE TxEscrowTransfers (agent, escrow_expiration, escrow_id, fee, fee_symbol, from, hbd_amount, hive_amount, ID, json_meta, ratification_deadline, timestamp, to, tx_id);
# CREATE TABLE TxFeeds (exchange_rate_base, exchange_rate_quote, ID, publisher, timestamp, tx_id);
# CREATE TABLE TxLimitOrdersCancels (ID, orderid, owner, timestamp, tx_id);
# CREATE TABLE TxLimitOrdersCreates (amount_to_sell, amount_to_sell_symbol, exchange_rate, exchange_rate_base, exchange_rate_quote, expiration, fill_or_kill, ID, min_to_receive, min_to_receive_symbol, orderid, owner, timestamp, tx_id);
# CREATE TABLE TxPows (block_id, ID, timestamp, tx_id, worker_account);
# CREATE TABLE TxProposalCreates (creator, daily_pay, daily_pay_symbol, end_date, ID, permlink, receiver, start_date, subject, timestamp, tx_id);
# CREATE TABLE TxProposalRemoves (extensions, ID, proposal_ids, proposal_owner, timestamp, tx_id);
# CREATE TABLE TxProposalUpdates (creator, daily_pay, daily_pay_symbol, ID, permlink, proposal_id, subject, timestamp, tx_id);
# CREATE TABLE TxProposalVoteUpdates (approve, extensions, ID, proposal_ids, timestamp, tx_id, voter);
# CREATE TABLE TxRecurrentTransfers (amount, amount_symbol, executions, extensions, from, ID, memo, recurrence, timestamp, to, tx_id);
# CREATE TABLE TxTransfers (amount, amount_symbol, from, ID, memo, request_id, timestamp, to, tx_id, type);
# CREATE TABLE TxVotes (author, ID, permlink, timestamp, tx_id, voter, weight);
# CREATE TABLE TxWithdraws (account, ID, timestamp, tx_id, vesting_shares);
# CREATE TABLE TxWithdrawVestingRoutes (auto_vest, from_account, ID, percent, timestamp, to_account, tx_id);
# CREATE TABLE TxWitnessSetProperties (extensions, ID, owner, props, timestamp, tx_id);
# CREATE TABLE TxWitnessUpdates (block_signing_key, ID, owner, props_account_creation_fee, props_hbd_interest_rate, props_maximum_block_size, timestamp, tx_id, url);
# CREATE TABLE VOAccountCreateds (block_num, creator, ID, initial_delegation, initial_delegation_symbol, initial_vesting_shares, initial_vesting_shares_symbol, new_account_name, timestamp);
# CREATE TABLE VOAuthorRewards (author, block_num, hbd_payout, hive_payout, ID, permlink, timestamp, vesting_payout);
# CREATE TABLE VOChangedRecoveryAccounts (account, block_num, ID, new_recovery_account, old_recovery_account, timestamp);
# CREATE TABLE VOClearNullAccountBalances (block_num, ID, timestamp, total_cleared);
# CREATE TABLE VOCollateralizedConvertImmediateConversions (block_num, hbd_out, ID, owner, requestid, timestamp);
# CREATE TABLE VOCommentBenefactorRewards (author, benefactor, block_num, hbd_payout, hive_payout, ID, permlink, timestamp, vesting_payout);
# CREATE TABLE VOCommentPayoutUpdates (author, block_num, ID, permlink, timestamp);
# CREATE TABLE VOCommentRewards (author, block_num, ID, payout, payout_symbol, permlink, timestamp);
# CREATE TABLE VOCurationRewards (author, block_num, curator, ID, permlink, reward, reward_symbol, timestamp);
# CREATE TABLE VODelayedVotings (block_num, ID, timestamp, voter, votes);
# CREATE TABLE VODHFConversions (block_num, hbd_amount_out, hive_amount_in, ID, timestamp, treasury);
# CREATE TABLE VODHFFundings (additional_funds, additional_funds_symbol, block_num, ID, timestamp, treasury);
# CREATE TABLE VOEscrowApproveds (agent, block_num, escrow_id, fee, fee_symbol, from, ID, timestamp, to);
# CREATE TABLE VOEscrowRejecteds (agent, block_num, escrow_id, fee, fee_symbol, from, hbd_amount, hive_amount, ID, timestamp, to);
# CREATE TABLE VOExpiredAccountNotifications (account, block_num, ID, timestamp);
# CREATE TABLE VOFillCollateralizedConvertRequests (amount_in, amount_in_symbol, amount_out, amount_out_symbol, block_num, excess_collateral, excess_collateral_symbol, ID, owner, requestid, timestamp);
# CREATE TABLE VOFillConvertRequests (amount_in, amount_in_symbol, amount_out, amount_out_symbol, block_num, ID, owner, requestid, timestamp);
# CREATE TABLE VOFillOrders (block_num, current_orderid, current_owner, current_pays, current_pays_symbol, ID, open_orderid, open_owner, open_pays, open_pays_symbol, timestamp);
# CREATE TABLE VOFillRecurrentTransfers (amount, amount_symbol, block_num, from, ID, memo, remaining_executions, timestamp, to);
# CREATE TABLE VOFillTransferFromSavings (amount, amount_symbol, block_num, from, ID, memo, requestid, timestamp, to);
# CREATE TABLE VOFillVestingWithdraws (block_num, deposited, deposited_symbol, from_account, ID, timestamp, to_account, withdrawn, withdrawn_symbol);
# CREATE TABLE VOHardforkHiveRestores (account, block_num, hbd_transferred, hive_transferred, ID, timestamp, treasury);
# CREATE TABLE VOHardforkHives (account, block_num, ID, sbd_transferred, steem_transferred, timestamp, total_steem_from_vests, vests_converted);
# CREATE TABLE VOHardforks (block_num, hardfork_id, ID, timestamp);
# CREATE TABLE VOInterests (block_num, ID, interest, owner, timestamp);
# CREATE TABLE VOLimitOrderCancelleds (amount_back, amount_back_symbol, block_num, ID, seller, timestamp);
# CREATE TABLE VOLiquidityRewards (block_num, ID, owner, payout, payout_symbol, timestamp);
# CREATE TABLE VOPowRewards (block_num, ID, reward, reward_symbol, timestamp, worker);
# CREATE TABLE VOProducerRewards (block_num, ID, producer, timestamp, vesting_shares);
# CREATE TABLE VOProposalFees (block_num, creator, fee, fee_symbol, ID, proposal_id, timestamp, treasury);
# CREATE TABLE VOProposalPays (block_num, ID, payment, payment_symbol, proposal_id, receiver, timestamp);
# CREATE TABLE VOReturnVestingDelegations (account, amount, amount_symbol, block_num, ID, timestamp);
# CREATE TABLE VOShutdownWitnesses (block_num, ID, owner, timestamp);
# CREATE TABLE VOSPSConverts (block_num, fund_account, hbd_amount_out, hbd_amount_out_symbol, hive_amount_in, hive_amount_in_symbol, ID, timestamp);
# CREATE TABLE VOSPSFunds (additional_funds, additional_funds_symbol, block_num, ID, timestamp);
# CREATE TABLE VOTransferToVestingCompleteds (block_num, from_account, hive_vested, hive_vested_symbol, ID, timestamp, to_account, vesting_shares_received, vesting_shares_received_symbol);
# CREATE TABLE Witnesses (account_creation_fee, account_creation_fee_symbol, created, hardfork_time_vote, hardfork_version_vote, hbd_exchange_rate_base, hbd_exchange_rate_base_symbol, hbd_exchange_rate_quote, hbd_exchange_rate_quote_symbol, hbd_interest_rate, last_aslot, last_confirmed_block_num, last_hbd_exchange_update, maximum_block_size, name, running_version, signing_key, total_missed, url, votes, votes_count);
