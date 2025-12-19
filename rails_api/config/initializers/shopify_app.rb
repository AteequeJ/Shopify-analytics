ShopifyApp.configure do |config|
  config.application_name = "My Shopify App"
  config.api_key = ENV.fetch('SHOPIFY_API_KEY', '').presence
  config.secret = ENV.fetch('SHOPIFY_API_SECRET', '').presence
  config.old_secret = ""
  config.scope = "read_products, read_orders, read_inventory" # Consult this list
  config.embedded_app = true
  config.after_authenticate_job = false
  config.api_version = "2023-10"
  config.shop_session_repository = 'Shop'
  config.reauth_on_access_scope_changes = true
end
