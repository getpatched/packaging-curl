#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
cat > "$work/consumer.c" <<'C'
#include <stdio.h>
#include <curl/curl.h>

int main(int argc, char **argv)
{
    if (argc != 2 || curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK)
        return 1;

    CURL *client = curl_easy_init();
    if (client == NULL) {
        curl_global_cleanup();
        return 1;
    }

    CURLcode result = curl_easy_setopt(client, CURLOPT_URL, argv[1]);
    if (result == CURLE_OK)
        result = curl_easy_setopt(client, CURLOPT_PROTOCOLS_STR, "file");
    if (result == CURLE_OK)
        result = curl_easy_perform(client);
    if (result != CURLE_OK)
        fprintf(stderr, "%s\n", curl_easy_strerror(result));

    curl_easy_cleanup(client);
    curl_global_cleanup();
    return result == CURLE_OK ? 0 : 1;
}
C
cc -Wall -Wextra -Werror "$work/consumer.c" -o "$work/consumer" -lcurl
printf '%s\n' 'libcurl compatibility check' > "$work/input"
"$work/consumer" "file://$work/input" > "$work/output"
cmp "$work/input" "$work/output"
