// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Matt C',
  tagline: 'So long, and thanks for all the bits',
  favicon: 'pal_flag_fav.png',

  // Set the production url of your site here
  url: 'https://www.mattcompton.dev',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  trailingSlash: true,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
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
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          //editUrl:
           // 'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          //editUrl:
          //  'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
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
      image: 'img/pal_flag_fav.png',
      navbar: {
        title: 'Matt C',
        logo: {
          alt: 'My Site Logo',
          src: 'pal_flag_fav.png',
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
          /*{
            href: 'https://github.com/facebook/docusaurus',
            label: 'GitHub',
            position: 'right',
          },*/
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
