module Main exposing (..)

import Browser
import Element
import Element.Background as Background
import Element.Border as Border
import Element.Font as Font
import Element.Input as Input
import Html exposing (Html, button, div, p, text, textarea)
import Html.Attributes exposing (size, style)
import Html.Events exposing (onClick)
import Http
import Json.Decode as D
import Task



-- MAIN


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }



-- MODEL


type alias Model =
    { inputText : String
    , outputText : Maybe String
    , error : Maybe Http.Error
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model "" Nothing Nothing, Cmd.none )



-- UPDATE


type Msg
    = InputChanged String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputChanged txt ->
            ( { model | inputText = txt }
            , Cmd.none
            )



-- Commands
-- extractData : Cmd Msg
-- extractData file =
--     Http.request
--         { method = "POST"
--         , headers = []
--         , url = "http://localhost:8080/"
--         , body = Http.multipartBody [ Http.filePart "image" file ]
--         , expect = Http.expectJson GotAnalysisResponse personalDetailsDecoder
--         , timeout = Just 60000
--         , tracker = Nothing
--         }
-- VIEW


view : Model -> Html Msg
view model =
    Element.layout
        [ Element.width Element.fill
        , Element.spaceEvenly
        , Background.color (Element.rgb 255 0 254)
        , Font.family [Font.typeface "Comic Sans"]
        ]
    <|
        Element.column [ Element.width Element.fill ]
            [ Element.row [ Element.width Element.fill ]
                [ Element.el
                    [ Element.alignLeft
                    , Element.width Element.fill
                    , Element.padding 10
                    ]
                  <|
                    Input.multiline
                        [ Background.color <| Element.rgb 250 255 9
                        , Element.width <| Element.fill
                        , Element.height <| Element.px 500
                        ]
                        { onChange = InputChanged
                        , text = model.inputText
                        , placeholder =
                            Just <|
                                Input.placeholder [] <|
                                    Element.text "Put your text here..."
                        , label = Input.labelHidden ""
                        , spellcheck = False
                        }

                , Element.el
                    [ Element.alignRight
                    , Element.width Element.fill
                    , Element.padding 10
                    ]
                  <|
                    Input.multiline
                        [ Background.color <| Element.rgb 250 255 9
                        , Element.spacing 100
                        , Element.width <| Element.fill
                        , Element.height <| Element.px 500
                        ]
                        { onChange = InputChanged
                        , text = Maybe.withDefault "" model.outputText
                        , placeholder =
                            Just <|
                                Input.placeholder [] <|
                                    Element.text "Output text will appear here"
                        , label = Input.labelHidden ""
                        , spellcheck = False
                        }
                ]
            , Element.row [ Element.width Element.fill ]
                [ Element.el
                    [ Element.centerX
                    ]
                  <|
                    Input.button
                        [ Background.color <|
                            Element.rgb 118 118 118
                        , Border.width 1
                        , Border.color <| Element.rgb 0 0 0
                        , Border.rounded 3
                        , Element.padding 10
                        ]
                        { onPress = Nothing, label = Element.text "Simplify" }
                ]
            ]



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none
