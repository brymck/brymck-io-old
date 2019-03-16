load("@io_bazel_rules_go//go:def.bzl", "go_library")
load("@bazel_gazelle//:def.bzl", "gazelle")

# gazelle:prefix github.com/brymck/brymck-io/src/api
gazelle(name = "gazelle")

go_library(
    name = "go_default_library",
    srcs = [
        "handlers.go",
        "main.go",
        "middleware.go",
        "rpc.go",
    ],
    importpath = "github.com/brymck/brymck-io/src/api",
    visibility = ["//visibility:private"],
    deps = [
        "//genproto:go_default_library",
        "@com_github_google_uuid//:go_default_library",
        "@com_github_gorilla_mux//:go_default_library",
        "@com_github_pkg_errors//:go_default_library",
        "@com_github_sirupsen_logrus//:go_default_library",
        "@io_opencensus_go//plugin/ocgrpc:go_default_library",
        "@io_opencensus_go//plugin/ochttp:go_default_library",
        "@io_opencensus_go//plugin/ochttp/propagation/b3:go_default_library",
        "@org_golang_google_grpc//:go_default_library",
    ],
)

load("@io_bazel_rules_docker//go:image.bzl", "go_image")

go_image(
    name = "api",
    embed = [":go_default_library"],
    visibility = ["//visibility:public"],
)
