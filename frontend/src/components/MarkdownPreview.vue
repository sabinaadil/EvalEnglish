<template>
    <div class="prose prose-sm max-w-none" v-html="renderedMarkdown"></div>
</template>

<script>
import { marked } from "marked";

export default {
    name: "MarkdownPreview",
    props: {
        content: {
            type: String,
            required: true,
        },
    },
    computed: {
        renderedMarkdown() {
            return marked.parse(this.content || "");
        },
    },
};
</script>

<style scoped></style>