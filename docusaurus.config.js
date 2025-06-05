// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Matt C',
  tagline: 'So long, and thanks for all the bits',
  favicon: 'siseor.jpg',

  url: 'https://mattcompton.dev',
  baseUrl: '/',

  trailingSlash: true,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/SomethingGeneric/website/docs/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/SomethingGeneric/website/blog/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'homelab',
        path: 'homelab',
        routeBasePath: 'homelab',
        sidebarPath: require.resolve('./sidebars.js'),
        // ... other options
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'techjournals',
        path: 'techjournals',
        routeBasePath: 'techjournals',
        sidebarPath: require.resolve('./sidebars.js'),
        // ... other options
      },
    ],
  ],

  scripts: [
    {
      src: 'https://rybbit.xhec.dev/api/script.js',
      defer: true,
      'data-site-id': '2',
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      mermaid: {
        theme: {light: 'neutral', dark: 'forest'},
      },
      prism: {
        additionalLanguages: ['bash'],
        theme: prismThemes.dracula,
      },
      // Replace with your project's social card
      image: 'img/siseor.jpg',
      navbar: {
        title: 'Matt C',
        logo: {
          alt: 'My Site Logo',
          src: 'siseor.jpg',
        },
        items: [
          {
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'Pages',
          },
          {
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'Homelab',
            docsPluginId: 'homelab',
          },
          {
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'Tech Journals',
            docsPluginId: 'techjournals',
          },
          {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/SomethingGeneric',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        /*links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Tutorial',
                to: '/docs/index',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/SomethingGeneric',
              },
            ],
          },
        ],*/
        copyright: `Copyright © ${new Date().getFullYear()} Matt C. Built with a bit of Docusaurus.`,
      },
    }),
};

module.exports = config;
