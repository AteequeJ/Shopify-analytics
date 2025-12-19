require 'bundler/setup'

gems = %w[rails puma rack-cors shopify_app shopify_api httparty dotenv-rails sqlite3 listen spring]

gems.each do |g|
  begin
    require g
    puts "Loaded #{g}"
  rescue LoadError => e
    puts "Failed to load #{g}: #{e.message}"
  rescue => e
    puts "Error loading #{g}: #{e.message}"
  end
end
