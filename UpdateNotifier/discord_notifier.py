from discord_webhook import DiscordEmbed, DiscordWebhook

from UpdateNotifier.config import discord_role_id, logger, ping, webhook_url

# Discord Limits
MAX_FIELDS_PER_EMBED = 25  # Discord allows max 25 fields per embed


def send_discord_notification(results: list[dict[str, str]], ping_user: bool) -> None:
    """
    Send a Discord notification with the list of services that have new updates.
    Splits messages into multiple embeds if necessary.

    :param results: List of services with new updates
    :type results: list[dict[str, str]]
    :param ping_user: Boolean indicating if the user should be pinged
    :type ping_user: bool
    """
    # If ping all is enabled, add the role mention to the content
    if ping:
        logger.debug("Ping is enabled.")
        if discord_role_id != "" and ping_user:
            logger.debug("Pinging Discord role.")
            webhook = DiscordWebhook(url=webhook_url, content=f"<@&{discord_role_id}>\n")
        else:
            if not ping_user:
                logger.debug("No major updates found.")
            else:
                logger.debug("No role ID is set.")
            webhook = DiscordWebhook(url=webhook_url)
    else:
        logger.debug("Ping is disabled.")
        if discord_role_id != "":
            logger.debug("Discord role ID is set.")
        if not ping_user:
            logger.debug("No major updates found, or no new services found.")
        webhook = DiscordWebhook(url=webhook_url)

    # Split results into batches of MAX_FIELDS_PER_EMBED
    for i in range(0, len(results), MAX_FIELDS_PER_EMBED):
        batch = results[i : i + MAX_FIELDS_PER_EMBED]
        logger.debug(f"Sending Discord notification with {len(batch)} services.")

        embed = DiscordEmbed(
            title="UpdateNotifier",
            description="### New updates\nThe following services have new updates:",
            color="03b2f8",
            url="https://github.com/gylfirst/UpdateNotifier",
        )

        for service in batch:
            embed.add_embed_field(
                name=f"**{service['name']}**",
                value=f"**Version:** {service['version']}\n**URL:** <{service['url']}>",
                inline=False,
            )

        embed.set_footer(
            text="by Matthieu Tourrette - Gylfirst",
            icon_url="https://avatars.githubusercontent.com/u/30391973?v=4",
        )
        embed.set_timestamp()

        webhook.add_embed(embed)

        # Send the webhook message
        try:
            response = webhook.execute()
            # Reset content for the next batch
            webhook.remove_embeds()
            webhook.content = ""
            if response.status_code != 200:
                logger.error(
                    f"Failed to send Discord notification: {response.status_code} {response.text}"
                )
        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
