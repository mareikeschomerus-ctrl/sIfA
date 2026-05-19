# Third-party licences

The offline build of the sIfA Tool — `Make your sIfA vX.X (offline).html` — inlines three third-party JavaScript libraries so the tool runs without an internet connection. All three are distributed under the MIT License. Their original copyright notices and the full MIT licence text are reproduced below, satisfying the attribution requirements of both the MIT licences and the Apache License 2.0 under which the sIfA Tool itself is released.

The online build (`Make your sIfA vX.X.html`) does not bundle these libraries; it loads them from a public CDN at runtime.

---

## React (v18.2.0)

**Source:** https://github.com/facebook/react
**Bundled file in the offline build:** `react.production.min.js`

```
MIT License

Copyright (c) Meta Platforms, Inc. and affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ReactDOM (v18.2.0)

**Source:** https://github.com/facebook/react
**Bundled file in the offline build:** `react-dom.production.min.js`

ReactDOM is part of the React project and is distributed under the same MIT License as React (reproduced above), with copyright held by Meta Platforms, Inc. and affiliates.

---

## Babel Standalone (v7.23.2)

**Source:** https://github.com/babel/babel
**Bundled file in the offline build:** `babel.min.js`

```
MIT License

Copyright (c) 2014-present Sebastian McKenzie and other contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
```

---

## Apache 2.0 compatibility note

The sIfA Tool as a whole is released under the Apache License 2.0. Bundling MIT-licensed components inside an Apache-2.0 distribution is permitted, provided the MIT notices above are preserved alongside the bundled code. This file, together with the `NOTICE` file at the repository root, satisfies that requirement.
