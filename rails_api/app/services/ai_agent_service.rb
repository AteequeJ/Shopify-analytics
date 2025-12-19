class AiAgentService
  include HTTParty
  base_uri ENV.fetch('PYTHON_SERVICE_URL', 'http://localhost:8000')

  def ask_question(store_id, question, token)
    begin
      response = self.class.post('/ask', body: {
        store_id: store_id,
        question: question,
        access_token: token
      }.to_json, headers: { 'Content-Type' => 'application/json' })

      if response.success?
        { success: true, data: JSON.parse(response.body) }
      else
        { success: false, error: "AI Service Error: #{response.code}" }
      end
    rescue StandardError => e
      { success: false, error: e.message }
    end
  end
end
