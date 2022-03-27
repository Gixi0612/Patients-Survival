mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
server.enableXsrfProtection=true\n\
\n\
" > ~/.streamlit/config.toml
