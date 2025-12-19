module Api
  module V1
    class QuestionsController < ApplicationController
      # Skip Shopify authentication for this specific endpoint for the assignment demonstration
      skip_before_action :verify_authenticity_token, raise: false
      
      # We are manually handling the store context via params, so we don't need the default login redirect
      # definition of `login_again_if_different_shop` or similar filters from the parent if they exist.

      def ask
        store_id = params[:store_id]
        question = params[:question]

        if store_id.blank? || question.blank?
          return render json: { error: "store_id and question are required" }, status: :bad_request
        end

        # In a real app, we would validate the store exists and is authenticated
        # shop = Shop.find_by(shopify_domain: store_id)
        # return render json: { error: "Shop not found" }, status: :not_found unless shop
        token = "mock_token_from_rails"

        # Forward to Python AI Service
        response = AiAgentService.new.ask_question(store_id, question, token)

        if response[:success]
          render json: response[:data]
        else
          render json: { error: response[:error] }, status: :service_unavailable
        end
      end
    end
  end
end
