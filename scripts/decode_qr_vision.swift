import CoreImage
import Foundation
import ImageIO
import Vision

guard CommandLine.arguments.count > 1 else {
    FileHandle.standardError.write(Data("usage: decode_qr_vision.swift IMAGE [IMAGE ...]\n".utf8))
    exit(2)
}

var failed = false
for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    if let image = CIImage(contentsOf: url),
       let detector = CIDetector(
           ofType: CIDetectorTypeQRCode,
           context: CIContext(options: [.useSoftwareRenderer: true]),
           options: [CIDetectorAccuracy: CIDetectorAccuracyHigh]
       ),
       let feature = detector.features(in: image).compactMap({ $0 as? CIQRCodeFeature }).first,
       let payload = feature.messageString {
        print("\(url.path)\t\(payload)")
        continue
    }
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        FileHandle.standardError.write(Data("cannot read image: \(path)\n".utf8))
        failed = true
        continue
    }
    let request = VNDetectBarcodesRequest()
    request.usesCPUOnly = true
    request.symbologies = [.qr]
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    do {
        try handler.perform([request])
        let payloads = (request.results ?? []).compactMap { $0.payloadStringValue }
        guard let payload = payloads.first else {
            FileHandle.standardError.write(Data("no QR payload found: \(path)\n".utf8))
            failed = true
            continue
        }
        print("\(url.path)\t\(payload)")
    } catch {
        FileHandle.standardError.write(Data("Vision failed for \(path): \(error)\n".utf8))
        failed = true
    }
}

if failed {
    exit(1)
}
