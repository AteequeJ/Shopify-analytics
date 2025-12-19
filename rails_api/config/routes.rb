Rails.application.routes.draw do
  root to: 'home#index'
  
  mount ShopifyApp::Engine, at: '/'

  namespace :api do
    namespace :v1 do
      post 'questions', to: 'questions#ask'
    end
  end
end
