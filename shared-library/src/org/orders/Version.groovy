package org.orders

// Pure helper class: testable without Jenkins.
class Version implements Serializable {
  static String tag(String branch, String build) {
    String safe = branch.replaceAll('[^A-Za-z0-9._-]', '-')
    return branch == 'main' ? "1.0.${build}" : "${safe}-${build}"
  }
}
