import { fusebox } from 'fuse-box';

declare var __dirname;
fusebox({
  target: 'browser',
  entry: 'src/main.js',
  webIndex: {
    template: 'src/index.html',
  },
  devServer: true,
}).runDev();
