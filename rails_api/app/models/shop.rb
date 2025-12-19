class Shop < ActiveRecord::Base
  include ShopifyApp::ShopSessionStorage
end
