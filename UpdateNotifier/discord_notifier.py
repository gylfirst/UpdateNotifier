from discord_webhook import DiscordEmbed, DiscordWebhook

from UpdateNotifier.config import discord_role_id, logger, webhook_url


def send_discord_notification(results: list[dict[str, str]]) -> None:
    """
    Send a Discord notification with the list of services that have new updates.

    :param results: List of services with new updates
    :type results: list[dict[str, str]]
    """
    webhook = DiscordWebhook(url=webhook_url, content=f"<@&{discord_role_id}>\n")
    # Create embed object for webhook
    embed = DiscordEmbed(
        title="UpdateNotifier",
        description="# New updates\nThe following services have new updates, please check below:",
        color="03b2f8",
        url="https://github.com/gylfirst/UpdateNotifier",
    )
    # Add embed fields
    for service in results:
        embed.add_embed_field(
            name=f"**{service['name']}**",
            value=f"**Version:** {service['version']}\n**URL:** <{service['url']}>",
        )
    # Set footer
    embed.set_footer(
        text="by Matthieu Tourrette - Gylfirst",
        icon_url="https://avatars.githubusercontent.com/u/30391973?v=4",
    )
    # Set timestamp
    embed.set_timestamp()
    # Add embed object to webhook
    webhook.add_embed(embed)
    # Execute webhook (send message)
    try:
        response = webhook.execute()
        if response.status_code != 200:
            logger.error(
                f"Failed to send Discord notification: {response.status_code} {response.text}"
            )
    except Exception as e:
        logger.error(f"Error sending Discord notification: {e}")
