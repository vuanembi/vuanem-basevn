gcloud functions \
  deploy basevn \
  --runtime=python37 \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=bivuanem@voltaic-country-280607.iam.gserviceaccount.com \
  --set-env-vars \
  WORKFLOW_TOKEN=$WORKFLOW_TOKEN,WEWORK_TOKEN=$WEWORK_TOKEN,TELEGRAM_TOKEN=$TELEGRAM_TOKEN \
  > deploy.log