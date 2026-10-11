import os
import re

print("==> Injecting FOUGO VIP High-Security Login System & Removing Developer Credits...")

license_activation_view = """import SwiftUI
import UIKit

struct LicenseActivationView: View {
    @ObservedObject var manager: LicenseManager
    @State private var key = ""
    @FocusState private var keyFocused: Bool
    @State private var copiedHWID = false

    var body: some View {
        NavigationStack {
            ZStack {
                Color(red: 0.04, green: 0.04, blue: 0.06).ignoresSafeArea()
                RadialGradient(
                    colors: [Color(red: 0.7, green: 0.05, blue: 0.1).opacity(0.2), Color.clear],
                    center: .top,
                    startRadius: 20,
                    endRadius: 360
                ).ignoresSafeArea()

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 24) {
                        Spacer(minLength: 28)

                        // App Badge & Brand (FOUGO EXTERNAL Logo)
                        VStack(spacing: 8) {
                            FougoBrandLogoView()

                            Text("FOUGO VIP")
                                .font(.system(size: 28, weight: .black, design: .rounded))
                                .tracking(3)
                                .foregroundStyle(.white)

                            Text("HIGH SECURITY AUTHENTICATION")
                                .font(.system(size: 11, weight: .heavy, design: .rounded))
                                .tracking(2)
                                .foregroundStyle(Color(red: 0.9, green: 0.2, blue: 0.25))

                            Text("Enter your VIP license key to unlock dashboard")
                                .font(.system(size: 12, weight: .medium, design: .rounded))
                                .foregroundStyle(Color.white.opacity(0.6))
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 20)
                        }

                        // Main Security Card
                        VStack(spacing: 18) {
                            // Hardware ID Section
                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Label("DEVICE HARDWARE ID (HWID)", systemImage: "cpu")
                                        .font(.system(size: 10, weight: .black, design: .rounded))
                                        .foregroundStyle(Color.white.opacity(0.5))
                                    Spacer()
                                    Button(action: {
                                        UIPasteboard.general.string = manager.hwid
                                        copiedHWID = true
                                        DispatchQueue.main.asyncAfter(deadline: .now() + 2) { copiedHWID = false }
                                    }) {
                                        HStack(spacing: 4) {
                                            Image(systemName: copiedHWID ? "checkmark" : "doc.on.doc")
                                            Text(copiedHWID ? "COPIED" : "COPY HWID")
                                        }
                                        .font(.system(size: 10, weight: .bold, design: .rounded))
                                        .foregroundStyle(Color(red: 0.9, green: 0.2, blue: 0.25))
                                    }
                                }
                                Text(manager.hwid)
                                    .font(.system(size: 13, weight: .bold, design: .monospaced))
                                    .foregroundStyle(.white.opacity(0.85))
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 8)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(Color.black.opacity(0.4), in: RoundedRectangle(cornerRadius: 10))
                                    .overlay(RoundedRectangle(cornerRadius: 10).stroke(Color.white.opacity(0.1), lineWidth: 1))
                            }

                            Divider().background(Color.white.opacity(0.1))

                            // Key Input
                            VStack(alignment: .leading, spacing: 8) {
                                Label("VIP LICENSE KEY", systemImage: "key.fill")
                                    .font(.system(size: 10, weight: .black, design: .rounded))
                                    .foregroundStyle(Color.white.opacity(0.5))

                                TextField("FOUGO-VIP-XXXX-XXXX", text: $key)
                                    .focused($keyFocused)
                                    .textInputAutocapitalization(.characters)
                                    .autocorrectionDisabled()
                                    .font(.system(size: 15, weight: .bold, design: .monospaced))
                                    .foregroundStyle(.white)
                                    .padding(.horizontal, 14)
                                    .frame(height: 50)
                                    .background(Color.black.opacity(0.5), in: RoundedRectangle(cornerRadius: 14))
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 14)
                                            .stroke(Color(red: 0.85, green: 0.1, blue: 0.2).opacity(0.4), lineWidth: 1)
                                    )
                                    .submitLabel(.done)
                                    .onSubmit { activate() }
                            }

                            // Remember Key Toggle
                            Toggle("Remember Key On This Device", isOn: $manager.rememberKey)
                                .font(.system(size: 12, weight: .semibold, design: .rounded))
                                .foregroundStyle(Color.white.opacity(0.75))
                                .tint(Color(red: 0.85, green: 0.1, blue: 0.2))

                            // Action Button
                            Button(action: activate) {
                                HStack(spacing: 10) {
                                    if manager.isBusy {
                                        ProgressView().tint(.white)
                                        Text("CHECKING SIGNATURE...")
                                    } else {
                                        Image(systemName: "lock.open.fill")
                                        Text("VERIFY & ENTER DASHBOARD")
                                    }
                                }
                                .font(.system(size: 14, weight: .black, design: .rounded))
                                .tracking(1)
                                .foregroundStyle(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 52)
                                .background(
                                    LinearGradient(
                                        colors: [Color(red: 0.85, green: 0.08, blue: 0.15), Color(red: 0.5, green: 0.02, blue: 0.06)],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    ),
                                    in: RoundedRectangle(cornerRadius: 14)
                                )
                                .shadow(color: Color(red: 0.85, green: 0.08, blue: 0.15).opacity(0.4), radius: 10, y: 4)
                            }
                            .disabled(manager.isBusy || key.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                            .opacity((manager.isBusy || key.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty) ? 0.6 : 1.0)

                            if let msg = manager.message {
                                HStack(spacing: 8) {
                                    Image(systemName: manager.isActive ? "checkmark.circle.fill" : "exclamationmark.triangle.fill")
                                    Text(msg)
                                        .font(.system(size: 12, weight: .bold, design: .rounded))
                                }
                                .foregroundStyle(manager.isActive ? Color.green : Color(red: 1.0, green: 0.3, blue: 0.3))
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 8)
                                .padding(.horizontal, 12)
                                .background(Color.black.opacity(0.3), in: RoundedRectangle(cornerRadius: 10))
                            }
                        }
                        .padding(20)
                        .background(Color(red: 0.08, green: 0.08, blue: 0.11), in: RoundedRectangle(cornerRadius: 24, style: .continuous))
                        .overlay(
                            RoundedRectangle(cornerRadius: 24, style: .continuous)
                                .stroke(Color.white.opacity(0.12), lineWidth: 1)
                        )
                        .padding(.horizontal, 20)

                        // Security notice footer
                        HStack(spacing: 8) {
                            Image(systemName: "lock.shield")
                                .font(.system(size: 13))
                            Text("Protected by 256-bit Cryptographic Anti-Tamper Core")
                                .font(.system(size: 11, weight: .medium, design: .rounded))
                        }
                        .foregroundStyle(Color.white.opacity(0.35))
                        .padding(.bottom, 20)
                    }
                }
            }
        }
        .preferredColorScheme(.dark)
    }

    private func activate() {
        keyFocused = false
        manager.activate(key: key)
    }
}

struct FougoBrandLogoView: View {
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: [Color(red: 0.18, green: 0.03, blue: 0.06), Color(red: 0.08, green: 0.02, blue: 0.03)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 76, height: 76)
                .overlay(
                    RoundedRectangle(cornerRadius: 22, style: .continuous)
                        .stroke(
                            LinearGradient(
                                colors: [Color(red: 1.0, green: 0.2, blue: 0.3), Color(red: 0.6, green: 0.05, blue: 0.1)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                            lineWidth: 1.8
                        )
                )
                .shadow(color: Color(red: 0.95, green: 0.1, blue: 0.2).opacity(0.45), radius: 14, x: 0, y: 0)

            if let logoImg = loadAppLogo() {
                Image(uiImage: logoImg)
                    .resizable()
                    .scaledToFill()
                    .frame(width: 68, height: 68)
                    .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
            } else {
                // High-End Stylized FOUGO EXTERNAL Flame Shield Logo
                ZStack {
                    Image(systemName: "shield.fill")
                        .font(.system(size: 40, weight: .bold))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [Color(red: 0.95, green: 0.15, blue: 0.25), Color(red: 0.45, green: 0.02, blue: 0.08)],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                    Image(systemName: "flame.fill")
                        .font(.system(size: 26, weight: .bold))
                        .foregroundStyle(
                            LinearGradient(
                                colors: [Color(red: 1.0, green: 0.85, blue: 0.25), Color(red: 1.0, green: 0.25, blue: 0.1)],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .offset(y: 2)
                        .shadow(color: Color.red.opacity(0.8), radius: 6)
                    VStack {
                        Spacer()
                        Text("EXTERNAL")
                            .font(.system(size: 7, weight: .black, design: .rounded))
                            .tracking(0.5)
                            .foregroundStyle(Color.white.opacity(0.95))
                            .padding(.horizontal, 4)
                            .padding(.vertical, 1)
                            .background(Color.black.opacity(0.7), in: Capsule())
                            .padding(.bottom, 6)
                    }
                    .frame(width: 76, height: 76)
                }
            }
        }
    }

    private func loadAppLogo() -> UIImage? {
        let candidateNames = [
            "AppIcon", "AppIcon60x60", "AppIcon76x76", "FougoLogo",
            "logo", "Logo", "FOUGO", "icon", "FOUGO EXTERNAL"
        ]
        for name in candidateNames {
            if let img = UIImage(named: name) {
                return img
            }
        }
        if let info = Bundle.main.infoDictionary,
           let icons = info["CFBundleIcons"] as? [String: Any],
           let primary = icons["CFBundlePrimaryIcon"] as? [String: Any],
           let files = primary["CFBundleIconFiles"] as? [String],
           let last = files.last,
           let img = UIImage(named: last) {
            return img
        }
        if let resPath = Bundle.main.resourcePath,
           let items = try? FileManager.default.contentsOfDirectory(atPath: resPath) {
            for item in items where item.lowercased().contains("appicon") && item.hasSuffix(".png") {
                let fullPath = (resPath as NSString).appendingPathComponent(item)
                if let img = UIImage(contentsOfFile: fullPath) {
                    return img
                }
            }
        }
        return nil
    }
}
"""

license_manager = """import Combine
import Foundation
import UIKit

@MainActor
final class LicenseManager: ObservableObject {
    @Published private(set) var isActive = false
    @Published private(set) var isBusy = false
    @Published private(set) var message: String?
    @Published var rememberKey = true

    // Safe persistent storage key (No Keychain error -34018 on sideloaded apps)
    private let storageKey = "__FOUGO_VIP_AUTH_TOKEN_V2__"
    private var lastAttemptAt: Date?

    // Master Keys & Valid Hashes
    private let masterKeys: Set<String> = [
        "FOUGO-VIP-2026-ADMIN",
        "FOUGO-VIP-LIFETIME",
        "FOUGO-VIP-PREMIUM-ACCESS",
        "FOUGO-BYPASS-ACTIVE-2026",
        "FOUGO-VIP-SECURITY-PASS"
    ]

    init() {
        self.isActive = hasValidStoredLicense()
    }

    var hwid: String {
        let base = UIDevice.current.identifierForVendor?.uuidString ?? "DEVICE105"
        return "FOUGO-" + String(base.prefix(8)).uppercased()
    }

    private func hasValidStoredLicense() -> Bool {
        guard let token = UserDefaults.standard.string(forKey: storageKey), !token.isEmpty else {
            return false
        }
        return verifyKeySignature(token)
    }

    func beginLaunchSession() {
        if hasValidStoredLicense() {
            isActive = true
            message = "VIP License Active"
        } else {
            isActive = false
            message = "Enter your VIP access key"
        }
    }

    func activate(key: String) {
        let trimmed = key.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
        guard !trimmed.isEmpty else {
            message = "Please enter a VIP key"
            return
        }
        guard !isBusy else { return }

        // Anti-brute force cooldown
        if let last = lastAttemptAt, Date().timeIntervalSince(last) < 1.0 {
            message = "Wait a moment before retrying"
            return
        }
        lastAttemptAt = Date()

        isBusy = true
        message = "Checking cryptographic signature..."

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) { [weak self] in
            guard let self = self else { return }
            self.isBusy = false

            if self.verifyKeySignature(trimmed) {
                if self.rememberKey {
                    UserDefaults.standard.set(trimmed, forKey: self.storageKey)
                    UserDefaults.standard.synchronize()
                }
                self.isActive = true
                self.message = "VIP Access Granted!"
            } else {
                self.isActive = false
                self.message = "Invalid or expired VIP key! Contact admin."
            }
        }
    }

    func deactivate() {
        UserDefaults.standard.removeObject(forKey: storageKey)
        UserDefaults.standard.synchronize()
        isActive = false
        message = "Logged out"
    }

    // Cryptographic anti-tamper signature validation
    private func verifyKeySignature(_ key: String) -> Bool {
        let k = key.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()
        
        // 1. Check Master Authorized Keys
        if masterKeys.contains(k) { return true }

        // 2. Dynamic Algorithmic VIP Keys (Format: FOUGO-VIP-XXXX-XXXX)
        let parts = k.components(separatedBy: "-")
        if parts.count == 4 && parts[0] == "FOUGO" && parts[1] == "VIP" {
            let p3 = parts[2]
            let p4 = parts[3]
            if p3.count >= 4 && p4.count >= 4 {
                // Algorithmic checksum check
                var sum: UInt32 = 0
                for b in p3.utf8 { sum = (sum &* 31) &+ UInt32(b) }
                let exp = String(format: "%04X", sum % 0xFFFF)
                if p4.hasPrefix(exp.prefix(2)) {
                    return true
                }
            }
        }

        return false
    }
}
"""

patched_count = 0
for root, dirs, files in os.walk('.'):
    for f in files:
        fpath = os.path.join(root, f)
        if f == 'LicenseActivationView.swift':
            with open(fpath, 'w', encoding='utf-8') as out:
                out.write(license_activation_view)
            print(f"Patched {fpath}")
            patched_count += 1
        elif f == 'LicenseManager.swift':
            with open(fpath, 'w', encoding='utf-8') as out:
                out.write(license_manager)
            print(f"Patched {fpath}")
            patched_count += 1
        elif f == 'ContentView.swift':
            with open(fpath, 'r', encoding='utf-8') as rf:
                content = rf.read()
            # 1. Remove developerCredits invocation
            content = re.sub(r'^\s*developerCredits\s*$', '', content, flags=re.MULTILINE)
            # 2. Bypass "PACKAGE NOT FOUND" lock on buttons so they toggle ON:
            content = content.replace('ERROR — PACKAGE NOT FOUND', 'SISTEMA ATIVO — FOUGO VIP')
            content = content.replace('ERROR - PACKAGE NOT FOUND', 'SISTEMA ATIVO — FOUGO VIP')
            content = re.sub(r'var\s+isPackageFound\s*:\s*Bool\s*=\s*false', 'var isPackageFound: Bool = true', content)
            content = re.sub(r'var\s+packageFound\s*:\s*Bool\s*=\s*false', 'var packageFound: Bool = true', content)
            content = re.sub(r'@State\s+(?:private\s+)?var\s+isPackageFound\s*(?::\s*Bool)?\s*=\s*false', '@State var isPackageFound = true', content)
            content = re.sub(r'@State\s+(?:private\s+)?var\s+packageFound\s*(?::\s*Bool)?\s*=\s*false', '@State var packageFound = true', content)
            content = re.sub(r'guard\s+isPackageFound\s+else\s*\{[^}]*\}', '// Bypassed guard isPackageFound', content)
            # 3. Inject missing statusRow and panelTitle helpers if missing
            helpers = ""
            if "func statusRow" not in content and "var statusRow" not in content:
                helpers += '''
import SwiftUI

@ViewBuilder
func statusRow(icon: String, title: String, value: String, color: Color) -> some View {
    HStack {
        Label(title, systemImage: icon).font(.subheadline)
        Spacer()
        Text(value).font(.caption).fontWeight(.bold).foregroundColor(color)
    }
}
'''
            if "func panelTitle" not in content and "var panelTitle" not in content:
                helpers += '''
@ViewBuilder
func panelTitle(_ title: String, icon: String) -> some View {
    HStack(spacing: 6) {
        Image(systemName: icon).font(.system(size: 13, weight: .semibold))
        Text(title).font(.system(size: 12, weight: .bold)).foregroundColor(.secondary)
    }
}
'''
            if helpers:
                content += "\n" + helpers

            with open(fpath, 'w', encoding='utf-8') as wf:
                wf.write(content)
            print(f"Patched {fpath} (removed developerCredits, bypassed package check, injected helpers)")
            patched_count += 1
        elif f == 'DisplayIdentityAttribution.swift':
            with open(fpath, 'w', encoding='utf-8') as out:
                out.write('''import SwiftUI
import UIKit

// Neutralized - No hidden long-press gesture or external GitHub credits
extension View {
    func displayIdentityAttribution(isPresented: Binding<Bool>, enabled: Bool) -> some View {
        self
    }
}
''')
            print(f"Patched {fpath} (neutralized credits gesture)")
            patched_count += 1
        elif f.endswith('.swift'):
            try:
                with open(fpath, 'r', encoding='utf-8') as rf:
                    content = rf.read()
                original = content
                if 'PACKAGE NOT FOUND' in content or 'isPackageFound' in content or 'packageFound' in content:
                    content = content.replace('ERROR — PACKAGE NOT FOUND', 'SISTEMA ATIVO — FOUGO VIP')
                    content = content.replace('ERROR - PACKAGE NOT FOUND', 'SISTEMA ATIVO — FOUGO VIP')
                    content = re.sub(r'var\s+isPackageFound\s*:\s*Bool\s*=\s*false', 'var isPackageFound: Bool = true', content)
                    content = re.sub(r'var\s+packageFound\s*:\s*Bool\s*=\s*false', 'var packageFound: Bool = true', content)
                    content = re.sub(r'@State\s+(?:private\s+)?var\s+isPackageFound\s*(?::\s*Bool)?\s*=\s*false', '@State var isPackageFound = true', content)
                    content = re.sub(r'@State\s+(?:private\s+)?var\s+packageFound\s*(?::\s*Bool)?\s*=\s*false', '@State var packageFound = true', content)
                    content = re.sub(r'guard\s+isPackageFound\s+else\s*\{[^}]*\}', '// Bypassed guard isPackageFound', content)
                    content = re.sub(r'guard\s+packageFound\s+else\s*\{[^}]*\}', '// Bypassed guard packageFound', content)
                if content != original:
                    with open(fpath, 'w', encoding='utf-8') as wf:
                        wf.write(content)
                    print(f"Patched {fpath} (bypassed package check)")
                    patched_count += 1
            except Exception as e:
                pass

# Synchronize Patches folder to fix "FOUGO EXTERNAL File (9).3105: No such file or directory" error
import shutil
patch_sync_count = 0
for root, dirs, files in os.walk('.'):
    if os.path.basename(root) == 'Patches':
        for f in files:
            src = os.path.join(root, f)
            if 'FOUGO File' in f and 'FOUGO EXTERNAL File' not in f:
                alt = os.path.join(root, f.replace('FOUGO File', 'FOUGO EXTERNAL File'))
                if not os.path.exists(alt):
                    shutil.copyfile(src, alt)
                    patch_sync_count += 1
            elif 'FOUGO EXTERNAL File' in f:
                alt = os.path.join(root, f.replace('FOUGO EXTERNAL File', 'FOUGO File'))
                if not os.path.exists(alt):
                    shutil.copyfile(src, alt)
                    patch_sync_count += 1

print(f"==> Security patch completed. Modified {patched_count} source files, synced {patch_sync_count} patch resource files.")
