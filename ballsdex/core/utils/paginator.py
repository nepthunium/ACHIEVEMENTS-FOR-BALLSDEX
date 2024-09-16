    async def format_page(self, menu: Pages, entries: list[tuple[Any, Any]]) -> discord.Embed:
        self.embed.clear_fields()
        if self.clear_description:
            self.embed.description = None
        if isinstance(entries, tuple):
            entries = [entries]
        for key, value in entries:
            self.embed.add_field(name=key, value=value, inline=self.inline)
        maximum = self.get_max_pages()
        if maximum > 1:
            text = f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
            self.embed.set_footer(text=text)

        return self.embed

# FIND YOUR "FieldPageSource" CLASS AND REPLACE THE format_page FUNCTION WITH THIS
