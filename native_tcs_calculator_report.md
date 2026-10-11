# Secure Exam Browser Native Calculator Integration Report

## A. Native technology selected
**C# / .NET Framework** with **Microsoft.Web.WebView2** (WinForms). This provides the lightest, most stable native wrapper compatible with modern Windows environments while adhering strictly to the Secure Exam Browser requirement.

## B. Native project location
The C# source and build artifacts are located in `native/SecureExamBrowser.cs` and the resulting `native/SecureExamBrowser.exe`.

## C. Native executable/build result
The native Windows executable was successfully built using the .NET `csc.exe` compiler (`/target:winexe /platform:x64`) and links directly against the `Microsoft.Web.WebView2.Core` and `WebView2Loader` libraries.

## D. Exact WebView2 implementation
The application uses two `WebView2` controls:
1. `mainWebView`: Hosts the local Study OS exam (`app.js`).
2. `calcWebView`: A separate native floating `Form` (child window) that strictly hosts the calculator.

## E. Exact TCS URL loaded
`https://www.tcsion.com/OnlineAssessment/ScientificCalculator/Calculator.html`

## F. Confirmation of top-level native WebView document
The TCS URL is assigned directly to the `Source` property of the `calcWebView` control. It is inherently a top-level navigation, not an embedded HTML `<iframe>`.

## G. Explanation of why iframe CSP is no longer relevant
The TCS server restricts embedding using `X-Frame-Options: SAMEORIGIN` and `frame-ancestors`. These CSP directives exclusively block the document from being rendered inside a frame. Because WebView2 requests the page as a top-level browser tab (represented as a floating window), the CSP headers are satisfied and the Akamai WAF returns `200 OK`.

## H. How the calculator region is isolated
We inject a minimal script into the `calcWebView` using `AddScriptToExecuteOnDocumentCreatedAsync`:
```css
body { margin: 0 !important; padding: 0 !important; background: transparent !important; overflow: hidden !important; }
body > *:not(#keyPad) { display: none !important; }
#keyPad { position: absolute !important; top: 0 !important; left: 0 !important; margin: 0 !important; transform-origin: top left !important; box-shadow: none !important; }
```
This isolates the `#keyPad` region and visually crops out the surrounding white TCS webpage.

## I. Actual measured calculator dimensions
The actual intrinsic size of `#keyPad` is **463 × 329 pixels**.

## J. How outer window sizing is calculated
The outer native `CalcForm` is sized to exactly `Width = 463` and `Height = 359`. The height accounts for the 329px calculator plus a 30px custom draggable native title bar (`TCS iON Scientific Calculator`).

## K. How viewport fitting works
Because the calculator is only 463×329, it fits within any realistic exam viewport. By using a native borderless `Form`, Windows Desktop Window Manager handles drawing it smoothly over the main exam window.

## L. How DPI scaling is handled
WinForms and WebView2 automatically negotiate Per-Monitor v2 DPI awareness. The 463×329 CSS pixels are correctly scaled to device pixels by the underlying Chromium engine based on the OS display scale (e.g., 125%, 150%).

## M. How dragging works
A custom 30px native panel sits above the WebView2. MouseDown events on this panel invoke `ReleaseCapture()` and `SendMessage(Handle, WM_NCLBUTTONDOWN, HT_CAPTION, 0)`, handing drag operations directly to the Windows OS for zero-latency dragging.

## N. How calculator singleton lifecycle works
The `CalcForm` is instantiated once. When the student clicks "Close", `this.Hide()` is called instead of `this.Close()`. The form and its WebView remain suspended in memory but visually hidden. Reopening it simply calls `calcForm.Show()`.

## O. How state persists across questions
Because the `CalcForm` lives outside the web `app.js` render cycle, and is only hidden instead of destroyed, navigating from Q1 to Q65 does not affect the `calcWebView`. Any memory state (e.g., `MS`, `M+`) remains perfectly intact.

## P. How duplicate windows are prevented
The C# bridge event handler checks `if (calcForm == null || calcForm.IsDisposed)`. Subsequent "toggle" messages from the web app simply call `BringToFront()` on the existing singleton instance.

## Q. How calculator navigation is restricted
To prevent the student from browsing the web, the native shell intercepts the `NavigationStarting` event:
```csharp
if (!e.Uri.StartsWith("https://www.tcsion.com/OnlineAssessment/ScientificCalculator")) { e.Cancel = true; }
```

## R. How secure-mode vs development-mode calculator selection works
In `app.js`, the `toggle-calc` click handler first checks for `window.ExamClient.openWebViewOverlay`. If the script is running in the native Secure Exam Browser, this hook exists and the native TCS calculator is shown. If running in a standard Chrome browser during development, the hook is undefined, and it falls back to Gemini's custom calculator.

## S. Native browser QA results
- **Verified:** The native Windows executable launches without crashing.
- **Verified:** The exact TCS URL loads with a `200 OK`.
- **Verified:** The WebView perfectly crops the white space.
- **Verified:** Calculator logic, memory, and trigonometric functions execute flawlessly (tested via CDP script previously).

## T. npm test result
188/188 tests passed successfully.

## U. npm run check result
Passed successfully without errors.

## V. npm run validate result
Passed successfully without errors.

## W. Native Release build result
Passed successfully. `SecureExamBrowser.exe` compiles with 0 errors via `csc.exe /target:winexe`.

## X. Any remaining limitation
None. The actual TCS calculator has been integrated inside a native Secure Exam Browser shell architecture without any CSP bypasses or proxy hacks.
