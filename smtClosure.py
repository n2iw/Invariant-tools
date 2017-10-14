#!/usr/bin/python

import argparse
import os
import sys
import subprocess


FIRST_NUM = 1
LAST_NUM = 133 
SAMPLE = ' --sample-start=100'
# VISIBILITY = ' --std-visibility'
VISIBILITY = ' '
# SAMPLE = ' '
OPTIONS_TMP = ' --noversion --omit_from_output 0r --no_text_output --config_option daikon.FileIO.count_lines=false -o {}'
TEST_CLASS = ' daikonTestAll'
TEST_FILE = 'daikonTestAll.java'
COMPILE_CMDS = ['ant jar; ant all-classes-jar']
MAIN_PACKAGES = ['com.google.javascript.jscomp', 'com.google.javascript.rhino']
PACKAGES = [
        # 'com.google.javascript.jscomp'

        'com.google.javascript.jscomp',
        'com.google.javascript.jscomp.ant',
        'com.google.javascript.jscomp.deps',
        'com.google.javascript.jscomp.graph',
        'com.google.javascript.jscomp.jsonml',
        'com.google.javascript.jscomp.parsing',
        'com.google.javascript.jscomp.regex',
        'com.google.javascript.jscomp.testing',
        'com.google.javascript.jscomp.type',
        'com.google.javascript.jscomp.webservice.common',
        'com.google.javascript.rhino',
        'com.google.javascript.rhino.jstype',
        'com.google.javascript.rhino.testing'        
        ]

CLASSES = [
    'com.google.debugging.sourcemap.Base64',
    'com.google.debugging.sourcemap.Base64VLQ',
    'com.google.debugging.sourcemap.FilePosition',
    'com.google.debugging.sourcemap.SourceMapConsumer',
    'com.google.debugging.sourcemap.SourceMapConsumerFactory',
    'com.google.debugging.sourcemap.SourceMapConsumerV1',
    'com.google.debugging.sourcemap.SourceMapConsumerV2',
    'com.google.debugging.sourcemap.SourceMapConsumerV3',
    'com.google.debugging.sourcemap.SourceMapFormat',
    'com.google.debugging.sourcemap.SourceMapGenerator',
    'com.google.debugging.sourcemap.SourceMapGeneratorFactory',
    'com.google.debugging.sourcemap.SourceMapGeneratorV1',
    'com.google.debugging.sourcemap.SourceMapGeneratorV2',
    'com.google.debugging.sourcemap.SourceMapGeneratorV3',
    'com.google.debugging.sourcemap.SourceMapLineDecoder',
    'com.google.debugging.sourcemap.SourceMapParseException',
    'com.google.debugging.sourcemap.SourceMapping',
    'com.google.debugging.sourcemap.SourceMappingReversable',
    'com.google.debugging.sourcemap.SourceMapSection',
    'com.google.debugging.sourcemap.SourceMapSupplier',
    'com.google.debugging.sourcemap.Util',
    'com.google.javascript.jscomp.AbstractCommandLineRunner',
    'com.google.javascript.jscomp.AbstractCompiler',
    'com.google.javascript.jscomp.AbstractMessageFormatter',
    'com.google.javascript.jscomp.AbstractPeepholeOptimization',
    'com.google.javascript.jscomp.AliasExternals',
    'com.google.javascript.jscomp.AliasKeywords',
    'com.google.javascript.jscomp.AliasStrings',
    'com.google.javascript.jscomp.AmbiguateProperties',
    'com.google.javascript.jscomp.AnalyzeNameReferences',
    'com.google.javascript.jscomp.AnalyzePrototypeProperties',
    'com.google.javascript.jscomp.AnonymousFunctionNamingCallback',
    'com.google.javascript.jscomp.AnonymousFunctionNamingPolicy',
    'com.google.javascript.jscomp.ant.AntErrorManager',
    'com.google.javascript.jscomp.ant.CompileTask',
    'com.google.javascript.jscomp.ant.Warning',
    'com.google.javascript.jscomp.AstChangeProxy',
    'com.google.javascript.jscomp.AstParallelizer',
    'com.google.javascript.jscomp.AstValidator',
    'com.google.javascript.jscomp.BasicErrorManager',
    'com.google.javascript.jscomp.ByPathWarningsGuard',
    'com.google.javascript.jscomp.CallGraph',
    'com.google.javascript.jscomp.ChainCalls',
    'com.google.javascript.jscomp.CheckAccessControls',
    'com.google.javascript.jscomp.CheckDebuggerStatement',
    'com.google.javascript.jscomp.CheckGlobalNames',
    'com.google.javascript.jscomp.CheckGlobalThis',
    'com.google.javascript.jscomp.CheckLevel',
    'com.google.javascript.jscomp.CheckLevelLegacy',
    'com.google.javascript.jscomp.CheckMissingGetCssName',
    'com.google.javascript.jscomp.CheckMissingReturn',
    'com.google.javascript.jscomp.CheckPathsBetweenNodes',
    'com.google.javascript.jscomp.CheckProvides',
    'com.google.javascript.jscomp.CheckRegExp',
    'com.google.javascript.jscomp.CheckRequiresForConstructors',
    'com.google.javascript.jscomp.CheckSideEffects',
    'com.google.javascript.jscomp.CheckSuspiciousCode',
    'com.google.javascript.jscomp.CheckUnreachableCode',
    'com.google.javascript.jscomp.CleanupPasses',
    'com.google.javascript.jscomp.ClosureCodeRemoval',
    'com.google.javascript.jscomp.ClosureCodingConvention',
    'com.google.javascript.jscomp.ClosureOptimizePrimitives',
    'com.google.javascript.jscomp.ClosureRewriteClass',
    'com.google.javascript.jscomp.CoalesceVariableNames',
    'com.google.javascript.jscomp.CodeChangeHandler',
    'com.google.javascript.jscomp.CodeConsumer',
    'com.google.javascript.jscomp.CodeGenerator',
    'com.google.javascript.jscomp.CodePrinter',
    'com.google.javascript.jscomp.CodingConvention',
    'com.google.javascript.jscomp.CodingConventions',
    'com.google.javascript.jscomp.CollapseAnonymousFunctions',
    'com.google.javascript.jscomp.CollapseProperties',
    'com.google.javascript.jscomp.CollapseVariableDeclarations',
    'com.google.javascript.jscomp.CombinedCompilerPass',
    'com.google.javascript.jscomp.CommandLineRunner',
    'com.google.javascript.jscomp.CompilationLevel',
    'com.google.javascript.jscomp.Compiler',
    'com.google.javascript.jscomp.CompilerInput',
    'com.google.javascript.jscomp.CompilerOptions',
    'com.google.javascript.jscomp.CompilerPass',
    'com.google.javascript.jscomp.ComposeWarningsGuard',
    'com.google.javascript.jscomp.ConcreteType',
    'com.google.javascript.jscomp.ConstCheck',
    'com.google.javascript.jscomp.ControlFlowAnalysis',
    'com.google.javascript.jscomp.ControlFlowGraph',
    'com.google.javascript.jscomp.ControlStructureCheck',
    'com.google.javascript.jscomp.ConvertToDottedProperties',
    'com.google.javascript.jscomp.CreateSyntheticBlocks',
    'com.google.javascript.jscomp.CrossModuleCodeMotion',
    'com.google.javascript.jscomp.CrossModuleMethodMotion',
    'com.google.javascript.jscomp.CssRenamingMap',
    'com.google.javascript.jscomp.CustomPassExecutionTime',
    'com.google.javascript.jscomp.DataFlowAnalysis',
    'com.google.javascript.jscomp.DeadAssignmentsElimination',
    'com.google.javascript.jscomp.DefaultPassConfig',
    'com.google.javascript.jscomp.DefinitionProvider',
    'com.google.javascript.jscomp.DefinitionSite',
    'com.google.javascript.jscomp.DefinitionsRemover',
    'com.google.javascript.jscomp.Denormalize',
    'com.google.javascript.jscomp.DependencyOptions',
    'com.google.javascript.jscomp.deps.DependencyInfo',
    'com.google.javascript.jscomp.deps.DepsFileParser',
    'com.google.javascript.jscomp.deps.DepsGenerator',
    'com.google.javascript.jscomp.deps.JsFileLineParser',
    'com.google.javascript.jscomp.deps.JsFileParser',
    'com.google.javascript.jscomp.deps.JsFunctionParser',
    'com.google.javascript.jscomp.deps.PathUtil',
    'com.google.javascript.jscomp.deps.SimpleDependencyInfo',
    'com.google.javascript.jscomp.deps.SortedDependencies',
    'com.google.javascript.jscomp.DevirtualizePrototypeMethods',
    'com.google.javascript.jscomp.DiagnosticGroup',
    'com.google.javascript.jscomp.DiagnosticGroups',
    'com.google.javascript.jscomp.DiagnosticGroupWarningsGuard',
    'com.google.javascript.jscomp.DiagnosticType',
    'com.google.javascript.jscomp.DisambiguateProperties',
    'com.google.javascript.jscomp.DotFormatter',
    'com.google.javascript.jscomp.EmptyMessageBundle',
    'com.google.javascript.jscomp.ErrorFormat',
    'com.google.javascript.jscomp.ErrorHandler',
    'com.google.javascript.jscomp.ErrorManager',
    'com.google.javascript.jscomp.ErrorPass',
    'com.google.javascript.jscomp.ExpandJqueryAliases',
    'com.google.javascript.jscomp.ExploitAssigns',
    'com.google.javascript.jscomp.ExportTestFunctions',
    'com.google.javascript.jscomp.ExpressionDecomposer',
    'com.google.javascript.jscomp.ExternExportsPass',
    'com.google.javascript.jscomp.ExtractPrototypeMemberDeclarations',
    'com.google.javascript.jscomp.FieldCleanupPass',
    'com.google.javascript.jscomp.FindExportableNodes',
    'com.google.javascript.jscomp.FlowSensitiveInlineVariables',
    'com.google.javascript.jscomp.FunctionArgumentInjector',
    'com.google.javascript.jscomp.FunctionInjector',
    'com.google.javascript.jscomp.FunctionNames',
    'com.google.javascript.jscomp.FunctionRewriter',
    'com.google.javascript.jscomp.FunctionToBlockMutator',
    'com.google.javascript.jscomp.FunctionTypeBuilder',
    'com.google.javascript.jscomp.GatherRawExports',
    'com.google.javascript.jscomp.GatherSideEffectSubexpressionsCallback',
    'com.google.javascript.jscomp.GenerateExports',
    'com.google.javascript.jscomp.GlobalNamespace',
    'com.google.javascript.jscomp.GlobalVarReferenceMap',
    'com.google.javascript.jscomp.GoogleCodingConvention',
    'com.google.javascript.jscomp.GoogleJsMessageIdGenerator',
    'com.google.javascript.jscomp.graph.AdjacencyGraph',
    'com.google.javascript.jscomp.graph.Annotatable',
    'com.google.javascript.jscomp.graph.Annotation',
    'com.google.javascript.jscomp.graph.DiGraph',
    'com.google.javascript.jscomp.graph.FixedPointGraphTraversal',
    'com.google.javascript.jscomp.graph.Graph',
    'com.google.javascript.jscomp.graph.GraphColoring',
    'com.google.javascript.jscomp.graph.GraphNode',
    'com.google.javascript.jscomp.graph.GraphPruner',
    'com.google.javascript.jscomp.graph.GraphReachability',
    'com.google.javascript.jscomp.graph.GraphvizGraph',
    'com.google.javascript.jscomp.graph.LatticeElement',
    'com.google.javascript.jscomp.graph.LinkedDirectedGraph',
    'com.google.javascript.jscomp.graph.LinkedUndirectedGraph',
    'com.google.javascript.jscomp.graph.StandardUnionFind',
    'com.google.javascript.jscomp.graph.SubGraph',
    'com.google.javascript.jscomp.graph.UndiGraph',
    'com.google.javascript.jscomp.graph.UnionFind',
    'com.google.javascript.jscomp.GroupVariableDeclarations',
    'com.google.javascript.jscomp.HotSwapCompilerPass',
    'com.google.javascript.jscomp.IgnoreCajaProperties',
    'com.google.javascript.jscomp.InferJSDocInfo',
    'com.google.javascript.jscomp.InlineCostEstimator',
    'com.google.javascript.jscomp.InlineFunctions',
    'com.google.javascript.jscomp.InlineObjectLiterals',
    'com.google.javascript.jscomp.InlineProperties',
    'com.google.javascript.jscomp.InlineSimpleMethods',
    'com.google.javascript.jscomp.InlineVariables',
    'com.google.javascript.jscomp.InstrumentFunctions',
    'com.google.javascript.jscomp.InvocationsCallback',
    'com.google.javascript.jscomp.JoinOp',
    'com.google.javascript.jscomp.JqueryCodingConvention',
    'com.google.javascript.jscomp.JsAst',
    'com.google.javascript.jscomp.JSError',
    'com.google.javascript.jscomp.JsMessage',
    'com.google.javascript.jscomp.JsMessageDefinition',
    'com.google.javascript.jscomp.JsMessageExtractor',
    'com.google.javascript.jscomp.JsMessageVisitor',
    'com.google.javascript.jscomp.JSModule',
    'com.google.javascript.jscomp.JSModuleGraph',
    'com.google.javascript.jscomp.jsonml.ErrorLevel',
    'com.google.javascript.jscomp.jsonml.JsonML',
    'com.google.javascript.jscomp.jsonml.JsonMLAst',
    'com.google.javascript.jscomp.jsonml.JsonMLError',
    'com.google.javascript.jscomp.jsonml.JsonMLException',
    'com.google.javascript.jscomp.jsonml.JsonMLUtil',
    'com.google.javascript.jscomp.jsonml.NodeUtil',
    'com.google.javascript.jscomp.jsonml.Reader',
    'com.google.javascript.jscomp.jsonml.SecureCompiler',
    'com.google.javascript.jscomp.jsonml.TagAttr',
    'com.google.javascript.jscomp.jsonml.TagType',
    'com.google.javascript.jscomp.jsonml.Validator',
    'com.google.javascript.jscomp.jsonml.Writer',
    'com.google.javascript.jscomp.JSSourceFile',
    'com.google.javascript.jscomp.JvmMetrics',
    'com.google.javascript.jscomp.LightweightMessageFormatter',
    'com.google.javascript.jscomp.LineNumberCheck',
    'com.google.javascript.jscomp.LinkedFlowScope',
    'com.google.javascript.jscomp.LiveVariablesAnalysis',
    'com.google.javascript.jscomp.LoggerErrorManager',
    'com.google.javascript.jscomp.MakeDeclaredNamesUnique',
    'com.google.javascript.jscomp.MarkNoSideEffectCalls',
    'com.google.javascript.jscomp.MaybeReachingVariableUse',
    'com.google.javascript.jscomp.MemoizedScopeCreator',
    'com.google.javascript.jscomp.MessageBundle',
    'com.google.javascript.jscomp.MessageFormatter',
    'com.google.javascript.jscomp.MethodCompilerPass',
    'com.google.javascript.jscomp.MinimizeExitPoints',
    'com.google.javascript.jscomp.MoveFunctionDeclarations',
    'com.google.javascript.jscomp.MustBeReachingVariableDef',
    'com.google.javascript.jscomp.NameAnalyzer',
    'com.google.javascript.jscomp.NameAnonymousFunctions',
    'com.google.javascript.jscomp.NameAnonymousFunctionsMapped',
    'com.google.javascript.jscomp.NameGenerator',
    'com.google.javascript.jscomp.NameReferenceGraph',
    'com.google.javascript.jscomp.NameReferenceGraphConstruction',
    'com.google.javascript.jscomp.NameReferenceGraphReport',
    'com.google.javascript.jscomp.NodeIterators',
    'com.google.javascript.jscomp.NodeNameExtractor',
    'com.google.javascript.jscomp.NodeTraversal',
    'com.google.javascript.jscomp.NodeUtil',
    'com.google.javascript.jscomp.Normalize',
    'com.google.javascript.jscomp.ObjectPropertyStringPostprocess',
    'com.google.javascript.jscomp.ObjectPropertyStringPreprocess',
    'com.google.javascript.jscomp.OptimizeArgumentsArray',
    'com.google.javascript.jscomp.OptimizeCalls',
    'com.google.javascript.jscomp.OptimizeParameters',
    'com.google.javascript.jscomp.OptimizeReturns',
    'com.google.javascript.jscomp.parsing.Annotation',
    'com.google.javascript.jscomp.parsing.Config',
    'com.google.javascript.jscomp.parsing.IRFactory',
    'com.google.javascript.jscomp.parsing.JsDocInfoParser',
    'com.google.javascript.jscomp.parsing.JsDocToken',
    'com.google.javascript.jscomp.parsing.JsDocTokenStream',
    'com.google.javascript.jscomp.parsing.NullErrorReporter',
    'com.google.javascript.jscomp.parsing.ParserRunner',
    'com.google.javascript.jscomp.parsing.TypeSafeDispatcher',
    'com.google.javascript.jscomp.PassConfig',
    'com.google.javascript.jscomp.PassFactory',
    'com.google.javascript.jscomp.PeepholeCollectPropertyAssignments',
    'com.google.javascript.jscomp.PeepholeFoldConstants',
    'com.google.javascript.jscomp.PeepholeFoldWithTypes',
    'com.google.javascript.jscomp.PeepholeOptimizationsPass',
    'com.google.javascript.jscomp.PeepholeRemoveDeadCode',
    'com.google.javascript.jscomp.PeepholeReplaceKnownMethods',
    'com.google.javascript.jscomp.PeepholeSimplifyRegExp',
    'com.google.javascript.jscomp.PeepholeSubstituteAlternateSyntax',
    'com.google.javascript.jscomp.PerformanceTracker',
    'com.google.javascript.jscomp.PhaseOptimizer',
    'com.google.javascript.jscomp.PrepareAst',
    'com.google.javascript.jscomp.PreprocessorSymbolTable',
    'com.google.javascript.jscomp.PrintStreamErrorManager',
    'com.google.javascript.jscomp.ProcessClosurePrimitives',
    'com.google.javascript.jscomp.ProcessCommonJSModules',
    'com.google.javascript.jscomp.ProcessDefines',
    'com.google.javascript.jscomp.ProcessTweaks',
    'com.google.javascript.jscomp.PropertyRenamingPolicy',
    'com.google.javascript.jscomp.PureFunctionIdentifier',
    'com.google.javascript.jscomp.RecordFunctionInformation',
    'com.google.javascript.jscomp.ReferenceCollectingCallback',
    'com.google.javascript.jscomp.regex.CaseCanonicalize',
    'com.google.javascript.jscomp.regex.CharRanges',
    'com.google.javascript.jscomp.regex.RegExpTree',
    'com.google.javascript.jscomp.Region',
    'com.google.javascript.jscomp.RemoveTryCatch',
    'com.google.javascript.jscomp.RemoveUnusedClassProperties',
    'com.google.javascript.jscomp.RemoveUnusedNames',
    'com.google.javascript.jscomp.RemoveUnusedPrototypeProperties',
    'com.google.javascript.jscomp.RemoveUnusedVars',
    'com.google.javascript.jscomp.RenameLabels',
    'com.google.javascript.jscomp.RenameProperties',
    'com.google.javascript.jscomp.RenamePrototypes',
    'com.google.javascript.jscomp.RenameVars',
    'com.google.javascript.jscomp.ReorderConstantExpression',
    'com.google.javascript.jscomp.ReplaceCssNames',
    'com.google.javascript.jscomp.ReplaceIdGenerators',
    'com.google.javascript.jscomp.ReplaceMessages',
    'com.google.javascript.jscomp.ReplaceMessagesForChrome',
    'com.google.javascript.jscomp.ReplaceStrings',
    'com.google.javascript.jscomp.RescopeGlobalSymbols',
    'com.google.javascript.jscomp.Result',
    'com.google.javascript.jscomp.RhinoErrorReporter',
    'com.google.javascript.jscomp.RuntimeTypeCheck',
    'com.google.javascript.jscomp.SanityCheck',
    'com.google.javascript.jscomp.Scope',
    'com.google.javascript.jscomp.ScopeCreator',
    'com.google.javascript.jscomp.ScopedAliases',
    'com.google.javascript.jscomp.ShadowVariables',
    'com.google.javascript.jscomp.ShowByPathWarningsGuard',
    'com.google.javascript.jscomp.SideEffectsAnalysis',
    'com.google.javascript.jscomp.SimpleDefinitionFinder',
    'com.google.javascript.jscomp.SimpleFunctionAliasAnalysis',
    'com.google.javascript.jscomp.SimpleRegion',
    'com.google.javascript.jscomp.SourceAst',
    'com.google.javascript.jscomp.SourceExcerptProvider',
    'com.google.javascript.jscomp.SourceFile',
    'com.google.javascript.jscomp.SourceInformationAnnotator',
    'com.google.javascript.jscomp.SourceMap',
    'com.google.javascript.jscomp.SpecializationAwareCompilerPass',
    'com.google.javascript.jscomp.SpecializeModule',
    'com.google.javascript.jscomp.StatementFusion',
    'com.google.javascript.jscomp.StrictModeCheck',
    'com.google.javascript.jscomp.StrictWarningsGuard',
    'com.google.javascript.jscomp.Strings',
    'com.google.javascript.jscomp.StripCode',
    'com.google.javascript.jscomp.SuppressDocWarningsGuard',
    'com.google.javascript.jscomp.SymbolTable',
    'com.google.javascript.jscomp.SyntacticScopeCreator',
    'com.google.javascript.jscomp.SyntheticAst',
    'com.google.javascript.jscomp.testing.SimpleSourceExcerptProvider',
    'com.google.javascript.jscomp.testing.TestErrorReporter',
    'com.google.javascript.jscomp.TightenTypes',
    'com.google.javascript.jscomp.Tracer',
    'com.google.javascript.jscomp.TransformAMDToCJSModule',
    'com.google.javascript.jscomp.type.ChainableReverseAbstractInterpreter',
    'com.google.javascript.jscomp.type.ClosureReverseAbstractInterpreter',
    'com.google.javascript.jscomp.type.FlowScope',
    'com.google.javascript.jscomp.type.ReverseAbstractInterpreter',
    'com.google.javascript.jscomp.type.SemanticReverseAbstractInterpreter',
    'com.google.javascript.jscomp.TypeCheck',
    'com.google.javascript.jscomp.TypedCodeGenerator',
    'com.google.javascript.jscomp.TypedScopeCreator',
    'com.google.javascript.jscomp.TypeInference',
    'com.google.javascript.jscomp.TypeInferencePass',
    'com.google.javascript.jscomp.TypeValidator',
    'com.google.javascript.jscomp.UnreachableCodeElimination',
    'com.google.javascript.jscomp.UseSite',
    'com.google.javascript.jscomp.VarCheck',
    'com.google.javascript.jscomp.VariableMap',
    'com.google.javascript.jscomp.VariableNameGenerator',
    'com.google.javascript.jscomp.VariableReferenceCheck',
    'com.google.javascript.jscomp.VariableRenamingPolicy',
    'com.google.javascript.jscomp.VariableVisibilityAnalysis',
    'com.google.javascript.jscomp.VerboseMessageFormatter',
    'com.google.javascript.jscomp.WarningLevel',
    'com.google.javascript.jscomp.WarningsGuard',
    'com.google.javascript.jscomp.webservice.common.AbstractWebServiceException',
    'com.google.javascript.jscomp.webservice.common.ErrorCode',
    'com.google.javascript.jscomp.webservice.common.Protocol',
    'com.google.javascript.jscomp.WhitelistWarningsGuard',
    'com.google.javascript.jscomp.XtbMessageBundle',
    'com.google.javascript.rhino.ErrorReporter',
    'com.google.javascript.rhino.InputId',
    'com.google.javascript.rhino.IR',
    'com.google.javascript.rhino.JSDocInfo',
    'com.google.javascript.rhino.JSDocInfoBuilder',
    'com.google.javascript.rhino.jstype.AllType',
    'com.google.javascript.rhino.jstype.ArrowType',
    'com.google.javascript.rhino.jstype.BooleanLiteralSet',
    'com.google.javascript.rhino.jstype.BooleanType',
    'com.google.javascript.rhino.jstype.CanCastToVisitor',
    'com.google.javascript.rhino.jstype.EnumElementType',
    'com.google.javascript.rhino.jstype.EnumType',
    'com.google.javascript.rhino.jstype.EquivalenceMethod',
    'com.google.javascript.rhino.jstype.ErrorFunctionType',
    'com.google.javascript.rhino.jstype.FunctionBuilder',
    'com.google.javascript.rhino.jstype.FunctionParamBuilder',
    'com.google.javascript.rhino.jstype.FunctionType',
    'com.google.javascript.rhino.jstype.IndexedType',
    'com.google.javascript.rhino.jstype.InstanceObjectType',
    'com.google.javascript.rhino.jstype.JSType',
    'com.google.javascript.rhino.jstype.JSTypeNative',
    'com.google.javascript.rhino.jstype.JSTypeRegistry',
    'com.google.javascript.rhino.jstype.ModificationVisitor',
    'com.google.javascript.rhino.jstype.NamedType',
    'com.google.javascript.rhino.jstype.NoObjectType',
    'com.google.javascript.rhino.jstype.NoResolvedType',
    'com.google.javascript.rhino.jstype.NoType',
    'com.google.javascript.rhino.jstype.NullType',
    'com.google.javascript.rhino.jstype.NumberType',
    'com.google.javascript.rhino.jstype.ObjectType',
    'com.google.javascript.rhino.jstype.ParameterizedType',
    'com.google.javascript.rhino.jstype.Property',
    'com.google.javascript.rhino.jstype.PropertyMap',
    'com.google.javascript.rhino.jstype.PrototypeObjectType',
    'com.google.javascript.rhino.jstype.ProxyObjectType',
    'com.google.javascript.rhino.jstype.RecordType',
    'com.google.javascript.rhino.jstype.RecordTypeBuilder',
    'com.google.javascript.rhino.jstype.RelationshipVisitor',
    'com.google.javascript.rhino.jstype.SimpleReference',
    'com.google.javascript.rhino.jstype.SimpleSlot',
    'com.google.javascript.rhino.jstype.SimpleSourceFile',
    'com.google.javascript.rhino.jstype.StaticReference',
    'com.google.javascript.rhino.jstype.StaticScope',
    'com.google.javascript.rhino.jstype.StaticSlot',
    'com.google.javascript.rhino.jstype.StaticSourceFile',
    'com.google.javascript.rhino.jstype.StaticSymbolTable',
    'com.google.javascript.rhino.jstype.StringType',
    'com.google.javascript.rhino.jstype.TemplateType',
    'com.google.javascript.rhino.jstype.TernaryValue',
    'com.google.javascript.rhino.jstype.UnionType',
    'com.google.javascript.rhino.jstype.UnionTypeBuilder',
    'com.google.javascript.rhino.jstype.UnknownType',
    'com.google.javascript.rhino.jstype.UnresolvedTypeExpression',
    'com.google.javascript.rhino.jstype.ValueType',
    'com.google.javascript.rhino.jstype.Visitor',
    'com.google.javascript.rhino.jstype.VoidType',
    'com.google.javascript.rhino.JSTypeExpression',
    'com.google.javascript.rhino.Node',
    'com.google.javascript.rhino.ScriptRuntime',
    'com.google.javascript.rhino.SimpleErrorReporter',
    'com.google.javascript.rhino.SourcePosition',
    'com.google.javascript.rhino.testing.AbstractStaticScope',
    'com.google.javascript.rhino.testing.Asserts',
    'com.google.javascript.rhino.testing.BaseJSTypeTestCase',
    'com.google.javascript.rhino.testing.MapBasedScope',
    'com.google.javascript.rhino.testing.TestErrorReporter',
    'com.google.javascript.rhino.Token',
    'com.google.javascript.rhino.TokenStream'
        ]

COMPARABILITY_FILES = [ ]
select_ppt_template = ' --ppt-select-pattern="{}"'
omit_ppt_template = ' --ppt-omit-pattern="{}"'
omit_ppt_options = ' --ppt-omit-pattern=Test\\W'
# omit_ppt_options = ' '

CHICORY_MEM = '3'
TARGET_MEM = '5'
DAIKON_MEM = '8'
QUEUE = 'u2-grid'
NCPUS =  3
WALL_TIME =  72 * 60

LOAD_JAVA = 'module load java/1.7.0_25; '

def generate_py(version, cmds, local=False, args=''):
    path = os.path.dirname(os.path.realpath(__file__))
    fileName = "{}.py".format(version)
    of = open(fileName, 'w')

    header = open(os.path.join(path, 'header.py'), 'r')
    of.write(header.read())
    header.close()

    of.write('args = "{}"\n\n'.format(args))
    of.write('cmds = [\n')
    commands = ["'''{}'''".format(x) for x in cmds]
    of.write(",\n".join(commands))

    # of.write('"echo"\n')
    of.write('\n]\n')

    if not local:
        footer1 = open(os.path.join(path, 'footer1.py'), 'r')
        of.write(footer1.read())
        footer1.close()

    footer2 = open(os.path.join(path, 'footer2.py'), 'r')
    of.write(footer2.read())
    footer2.close()
    
    of.close()
    os.chmod(fileName, 0755)

# def submit(version, queue, ncpus, wall_time, dry_run, include):
    # cmd = "submit --detach -v {0} -M -n{1} -N{1} -w{2}  -i {4} -i ./lib/  ./{3}.py".format(queue, ncpus, wall_time, version, include)
    # print(cmd)
    # if not dry_run:
        # out = subprocess.check_output(cmd, shell=True)
        # print(out)

def submit(version, queue, ncpus, wall_time, dry_run, include):
    # cmd = "submit --detach -v {0} -M -n{1} -N{1} -w{2}  -i {4} -i ./lib/  ./{3}.py".format(queue, ncpus, wall_time, version, include)
    cmd = []
    cmd.append("submit")
    cmd.append("--detach")
    cmd.append("-M")
    cmd.append("-v")
    cmd.append(queue)
    cmd.append("-n{}".format(ncpus))
    cmd.append("-N{}".format(ncpus))
    cmd.append("-w{}".format(wall_time))
    cmd.append("-i")
    cmd.append("./lib/")
    cmd.append("-i")
    cmd.append(include)
    cmd.append("./{}.py".format(version))
    print(' '.join(cmd))
    if not dry_run:
        out = subprocess.check_output(cmd)
        print(out)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tasks on project 'Closure'")

    # run buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Run fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Run buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    # commands to run
    parser.add_argument('task', help='task to run', choices=['copy', 'compile', 'run', 'sequence', 'online', 'frontend', 'daikon', 'split', 'splitOnline', 'splitDaikon', 'print', 'clean'])
    parser.add_argument('-C', '--chicory_memory', type=int, help='memory size', default=CHICORY_MEM)
    parser.add_argument('-D', '--daikon_memory', type=int, help='memory size', default=DAIKON_MEM)
    parser.add_argument('-T', '--target_memory', type=int, help='memory size', default=TARGET_MEM)
    parser.add_argument('-v', '--queue', help='Cluster queue to use', default=QUEUE)
    parser.add_argument('-n', '--ncpus', type=int, help='cpus to require', default=NCPUS)
    parser.add_argument('-w', '--wall-time', type=int, help='wall time', default=WALL_TIME)
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')
    parser.add_argument('-g', '--debug', help="use debug partation and 30 minutes wall time" , action='store_true')
    parser.add_argument('-l', '--local', help="run locally" , action='store_true')

    args = parser.parse_args()

    if args.first < FIRST_NUM:
        print "First bug number must be greater than or equal to {}".format(FIRST_NUM) 
        exit(1)

    if args.last > LAST_NUM:
        print "Last bug number must be less than or equal to {}".format(LAST_NUM)
        exit(1)


    if args.fixed:
        kind = 'fix'
    elif args.buggy:
        kind = 'buggy'
    else:
        kind = 'buggy'
        print 'Should provide --buggy or --fixed'

    DAIKON = '$PWD/lib/daikon.jar' 
    COMPARABILITY = ''
    for c in COMPARABILITY_FILES:
        COMPARABILITY += ' --comparability-file=$PWD/lib/{}'.format(c)

    ppts = ''
    for main_ppt in MAIN_PACKAGES:
        ppts += '^{}|'.format(main_ppt)
    select_ppt_option = select_ppt_template.format(ppts[:-1])

    if args.local:
        loadJava = ''
    else:
        loadJava = LOAD_JAVA

    if args.debug:
        args.wall_time = 30
        args.queue = 'u2-grid-debug'

    for i in range(args.first, args.last + 1):
        print '=' * 75
        print 'version ' + str(i)

        version = '{}_{}'.format(kind, i)
        JUNIT = '$PWD/{}/lib/junit.jar'.format(version)
        CP = '$PWD/{0}/build/compiler.jar:$PWD/{0}/build/lib/rhino.jar:$PWD/{0}/build/classes'.format(version)
        dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
        dtraceOutput = ' --dtrace-file=' + dtraceFile
        invFile = '{}_{}.inv.gz'.format(kind, i)
        OPTIONS = OPTIONS_TMP.format(invFile)

        cmds = []
        include = './{}/'.format(version)

        cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.chicory_memory)
        cmd += ' {}:{}:{}'.format(DAIKON, JUNIT, CP)
        cmd += ' daikon.Chicory '
        cmd += select_ppt_option  
        cmd += omit_ppt_options
        cmd += SAMPLE
        cmd += VISIBILITY
        cmd += COMPARABILITY
        if args.task == 'sequence':
            # do run daikon on cluster
            cmd += ' --heap-size={}g'.format(max(args.daikon_memory, args.target_memory))
            cmd += ' --daikon-args="{}"'.format(OPTIONS)
            cmd += dtraceOutput
            cmd += ' --daikon'
            cmd += TEST_CLASS
            cmds.append(cmd)
        elif args.task == 'online':
            #do run daikon online on cluster no intermedia dtrace file will be generated
            cmd += ' --heap-size={}g'.format(max(args.daikon_memory, args.target_memory))
            cmd += ' --daikon-args="{}"'.format(OPTIONS)
            cmd += ' --daikon-online'
            cmd += TEST_CLASS
            cmds.append(cmd)
        elif args.task == 'frontend':
            #do run daikon front end on cluster
            cmd += ' --heap-size={}g'.format(args.target_memory)
            cmd += dtraceOutput
            cmd += TEST_CLASS
            cmds.append(cmd)
        elif args.task == 'daikon':
            #run daikon on cluster
            cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.daikon_memory)
            cmd += ' {}'.format(DAIKON)
            cmd += ' daikon.Daikon'
            cmd += select_ppt_option  
            cmd += omit_ppt_options
            cmd += OPTIONS
            cmd += ' ' + dtraceFile
            cmds.append(cmd)

            include = './{}'.format(dtraceFile)
        elif args.task == 'splitDaikon':
            #run daikon on packages separatedly
            for main_ppt in PACKAGES:
                select_ppt_option = select_ppt_template.format("^" + main_ppt)
                invFile = '{}_{}_{}.inv.gz'.format(kind, i, main_ppt)
                OPTIONS = OPTIONS_TMP.format(invFile)
                omit_ppts = 'Test\\W|'
                for ppt in PACKAGES:
                    if ppt != main_ppt and ppt.find(main_ppt) != -1:
                        omit_ppts += '^{}|'.format(ppt)
                omit_ppt_options = omit_ppt_template.format(omit_ppts[:-1])

                cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.daikon_memory)
                cmd += ' ' + DAIKON
                cmd += ' daikon.Daikon'
                cmd += select_ppt_option  
                cmd += omit_ppt_options
                cmd += OPTIONS
                cmd += ' ' + dtraceFile
                cmds.append(cmd)

            include = './{}'.format(dtraceFile)
        elif args.task == 'split':
                #do run frontend and daikon on each classe
                for main_ppt in CLASSES:
                    # print(main_ppt)
                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, main_ppt)
                    dtraceOutput = ' --dtrace-file=' + dtraceFile
                    select_ppt_option = select_ppt_template.format("^" + main_ppt)
                    txtFile = '{}_{}.txt'.format(kind, i)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, main_ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)
                    omit_ppts = 'Test\\W|'
                    for ppt in CLASSES:
                        if ppt != main_ppt and ppt.find(main_ppt) != -1:
                            omit_ppts += '^{}|'.format(ppt)
                    omit_ppt_options = omit_ppt_template.format(omit_ppts[:-1])

                    cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.chicory_memory)
                    cmd += ' {}:{}:{}'.format(DAIKON, JUNIT, CP)
                    cmd += ' daikon.Chicory '
                    cmd += ' --heap-size={}g'.format(args.target_memory)
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += VISIBILITY
                    cmd += COMPARABILITY
                    cmd += dtraceOutput
                    cmd += TEST_CLASS
                    cmds.append(cmd)

                    cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.daikon_memory)
                    cmd += ' ' + DAIKON
                    cmd += ' daikon.Daikon'
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += OPTIONS
                    cmd += ' ' + dtraceFile
                    cmds.append(cmd)

                    # cmds.append('''if [ -f {} ]; then\n  rm {}\nfi'''.format(invFile, dtraceFile))
                    cmds.append('rm {}'.format(dtraceFile))

                    cmd = '{}java -d64 -Xmx{}g -cp '.format(loadJava, args.daikon_memory)
                    cmd += DAIKON
                    cmd += ' daikon.PrintInvariants '
                    cmd += invFile
                    cmd += ' >> {}'.format(txtFile)
                    cmds.append(cmd)

                    cmds.append('rm {}'.format(invFile))
        elif args.task == 'splitOnline':
                #do run daikon online on each packages
                for main_ppt in CLASSES:
                    # print(main_ppt)
                    # dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, main_ppt)
                    # dtraceOutput = ' --dtrace-file=' + dtraceFile
                    select_ppt_option = select_ppt_template.format("^" + main_ppt)
                    txtFile = '{}_{}.txt'.format(kind, i)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, main_ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)
                    omit_ppts = 'Test\\W|'
                    for ppt in CLASSES:
                        if ppt != main_ppt and ppt.find(main_ppt) != -1:
                            omit_ppts += '^{}|'.format(ppt)
                    omit_ppt_options = omit_ppt_template.format(omit_ppts[:-1])

                    cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.chicory_memory)
                    cmd += ' {}:{}:{}'.format(DAIKON, JUNIT, CP)
                    cmd += ' daikon.Chicory '
                    cmd += ' --heap-size={}g'.format(max(args.daikon_memory, args.target_memory))
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += VISIBILITY
                    cmd += COMPARABILITY
                    cmd += ' --daikon-online'
                    cmd += ' --daikon-args="{}"'.format(OPTIONS)
                    cmd += TEST_CLASS
                    cmds.append(cmd)

                    cmd = '{}java -d64 -Xmx{}g -cp '.format(loadJava, args.daikon_memory)
                    cmd += DAIKON
                    cmd += ' daikon.PrintInvariants '
                    cmd += invFile
                    cmd += ' >> {}'.format(txtFile)
                    cmds.append(cmd)

                    # cmds.append('rm {}'.format(invFile))

        elif args.task == 'splitPackages':
                #do run frontend and daikon on each packages
                for main_ppt in PACKAGES:
                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, main_ppt)
                    dtraceOutput = ' --dtrace-file=' + dtraceFile
                    select_ppt_option = select_ppt_template.format("^" + main_ppt)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, main_ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)
                    omit_ppts = 'Test\\W|'
                    for ppt in PACKAGES:
                        if ppt != main_ppt and ppt.find(main_ppt) != -1:
                            omit_ppts += '^{}|'.format(ppt)
                    omit_ppt_options = omit_ppt_template.format(omit_ppts[:-1])

                    cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.chicory_memory)
                    cmd += ' {}:{}:{}'.format(DAIKON, JUNIT, CP)
                    cmd += ' daikon.Chicory '
                    cmd += ' --heap-size={}g'.format(args.target_memory)
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += VISIBILITY
                    cmd += COMPARABILITY
                    cmd += dtraceOutput
                    cmd += TEST_CLASS
                    cmds.append(cmd)

                    cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.daikon_memory)
                    cmd += ' ' + DAIKON
                    cmd += ' daikon.Daikon'
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += OPTIONS
                    cmd += ' ' + dtraceFile
                    cmds.append(cmd)
        elif args.task == 'compile':
            #compile
            for cmd in COMPILE_CMDS:
                cmds.append("cd {};{}".format(version, cmd))
        elif args.task == 'copy':
            cmd = 'cp {} {}/test/'.format(TEST_FILE, version)
            cmds.append(cmd)
        elif args.task == 'run':
            #run directly
            cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.target_memory)
            cmd += ' {}:{}'.format(JUNIT, CP)
            cmd += TEST_CLASS
            cmds.append(cmd)
        elif args.task == 'print':
            # print invaraints

            cmd = '{}java -d64 -Xmx{}g -cp'.format(loadJava, args.daikon_memory)
            cmd += DAIKON
            cmd += ' daikon.PrintInvariants '
            cmd += invFile
            cmd += ' > ../{}.txt'.format(version)
            cmds.append(cmd)
        elif args.task == 'clean':
            # remove all dtrace files if corresponding inv files exist
            files = os.listdir(os.environ["PWD"])
            filesSet = set(files)
            for f in files:
                if f.startswith(version) and f.endswith('.dtrace.gz'):
                    invFile = f.replace('dtrace.gz', 'inv.gz')
                    if invFile in filesSet:
                        cmd = 'rm ' + f
                        print(cmd)
                        cmds.append(cmd)
        else:
            print "invalid command: " + task
            exit(1)

        generate_py(version, cmds, args.local, ' '.join(sys.argv))
        if args.local:
            execute = './{}.py'.format(version)
            print(execute)
            if not args.dry_run:
                subprocess.call(execute)
        else:
            submit(version, args.queue, args.ncpus, args.wall_time, args.dry_run, include)
