module.exports = {
  title: "Gitzer Documentation",
  tagline: "The tagline of my site",
  url: "https://IgnisDa.github.io",
  baseUrl: "/Gitzer/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "IgnisDa",
  projectName: "Gitzer",
  themeConfig: {
    defaultMode: "dark",
    navbar: {
      logo: {
        alt: "Gitzer Logo",
        src: "img/gitzer-logo.png",
      },
      items: [
        {
          to: "/",
          activeBasePath: "/",
          label: "Docs",
          position: "left",
        },
        {
          href: "https://github.com/IgnisDa/Gitzer",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      copyright: `Copyright © ${new Date().getFullYear()} Diptesh Choudhuri, Built with Docusaurus.`,
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          routeBasePath: "/",
          editUrl: "https://github.com/IgnisDa/Gitzer/edit/main/gitzer-docs/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
